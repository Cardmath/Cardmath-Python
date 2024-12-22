from auth.onboarding import create_onboarding_token, OnboardingSavingsRequest, get_onboarding_recommendation
from auth.recovery import request_password_recovery, PasswordResetForm, reset_password, PasswordResetRequest, create_email_verification_token, send_verification_email, verify_email
from auth.schemas import Token
from auth.schemas import User, UserCreate
from chat.endpoint import chat 
from chat.schemas import ChatRequest
from contextlib import asynccontextmanager
from creditcard.endpoints.download import download
from creditcard.endpoints.download import DownloadRequest, DownloadResponse
from creditcard.endpoints.extract import extract
from creditcard.endpoints.extract import ExtractRequest, ExtractResponse
from creditcard.endpoints.parse import parse
from creditcard.endpoints.parse import ParseRequest, ParseResponse
from creditcard.endpoints.read_database import CreditCardsDatabaseRequest, CreditCardsDatabaseResponse
from creditcard.endpoints.read_database import read_credit_cards_database
from creditcard.schemas import *
from database.sql_alchemy_db import sync_engine, get_sync_db, print_sql_schema, Base
from auth.secrets import load_essential_secrets
from dotenv import load_dotenv
from datetime import timedelta
from fastapi import Request, Depends, FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from insights.cache_context import CacheContext
from insights.heavyhitters import read_heavy_hitters
from insights.moving_averages import compute_categories_moving_averages
from insights.optimal_cards.endpoint import optimize_credit_card_selection_milp
from insights.schemas import HeavyHittersRequest, HeavyHittersResponse, CategoriesMovingAveragesRequest, CategoriesMovingAveragesResponse
from insights.schemas import OptimalCardsAllocationRequest, OptimalCardsAllocationResponse
from pathlib import Path
from payments.stripe_checkout_session import create_checkout_session, CheckoutSessionRequest, CheckoutSessionIDRequest, CheckoutSessionResponse, stripe_webhook, get_checkout_session
from sqlalchemy.orm import Session
from teller.schemas import AccessTokenSchema, PreferencesSchema
from typing import Annotated
import auth.utils as auth_utils
import database.auth.crud as auth_crud
import teller.endpoints as teller_endpoints

import logging
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    CacheContext.initialize(cache_ttl_seconds=3600)
    load_dotenv(override=True)
    load_essential_secrets()
    Base.metadata.create_all(bind=sync_engine)
    yield
    CacheContext.clear()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_sync_db)
) -> Token:
    user = auth_utils.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,           
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/register")
async def register_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_sync_db)
) -> Token:
    if auth_crud.get_user_by_email(db, form_data.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,           
            detail="Username is already taken",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = UserCreate(username=form_data.username, 
                email=form_data.username, 
                full_name=form_data.username,
                disabled=False,
                password=form_data.password)
    db_user = auth_crud.create_user(db, user)
    
    token = create_email_verification_token(user.email)
    BASE_URL = "cardmath.ai" if os.getenv("ENVIRONMENT", "prod") == "prod" else "localhost:3000"
    verification_link = f"https://{BASE_URL}/registration-steps?token={token}"
    
    send_verification_email(user.email, verification_link)
    
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/retry-email-verification")
async def retry_email_verification_endpoint(user: User = Depends(auth_utils.get_current_user), db: Session = Depends(get_sync_db)):
    token = create_email_verification_token(user.email)
    BASE_URL = "cardmath.ai" if os.getenv("ENVIRONMENT", "prod") == "prod" else "localhost:3000"
    verification_link = f"https://{BASE_URL}/registration-steps?token={token}"
    return await send_verification_email(user.email, verification_link)

@app.get("/verify-email")
async def verify_email_endpoint(token: str, db: Session = Depends(get_sync_db)):
    return await verify_email(token=token, db=db)

@app.post("/process_new_enrollment")
def process_new_enrollment(current_user: Annotated[User, Depends(auth_utils.get_current_user)],
                           db: Session = Depends(get_sync_db)):
    return teller_endpoints.process_new_enrollment(current_user, db)

@app.post("/receive_teller_enrollment")
def receive_teller_enrollment(current_user: Annotated[User, Depends(auth_utils.get_current_user)],
                 access_token: AccessTokenSchema,
                 db: Session = Depends(get_sync_db)):
    return teller_endpoints.receive_teller_enrollment(db=db, access_token=access_token, user=current_user) 

@app.post("/save_user_preferences")
def ingest_user_preferences(current_user: Annotated[User, Depends(auth_utils.get_current_user)],
                 preferences: PreferencesSchema,
                 db: Session = Depends(get_sync_db)):
    return teller_endpoints.ingest_user_preferences(preferences=preferences, db=db, user=current_user)

@app.post("/download")
def download_endpoint(request: DownloadRequest) -> DownloadResponse:
    return download(request)
    
@app.post("/extract")
def extract_endpoint(request: ExtractRequest, db: Session = Depends(get_sync_db)) -> ExtractResponse:
    return extract(request, db)

@app.post("/parse") 
def parse_endpoint(request: ParseRequest, db: Session = Depends(get_sync_db)) -> ParseResponse:
    return parse(request, db)

@app.post("/read_heavy_hitters") 
async def heavy_hitters_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], 
                   request: HeavyHittersRequest, db: Session = Depends(get_sync_db)) -> HeavyHittersResponse:
    return await read_heavy_hitters(db=db, user=current_user, request=request)

@app.post("/compute_categories_moving_averages")
async def compute_categories_moving_averages_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], 
                   request: CategoriesMovingAveragesRequest, db: Session = Depends(get_sync_db)) -> CategoriesMovingAveragesResponse:
    return await compute_categories_moving_averages(db=db, user=current_user, request=request)

@app.post("/read_credit_cards_database")
async def read_credit_cards_database_endpoint(request: CreditCardsDatabaseRequest, db: Session = Depends(get_sync_db)) -> CreditCardsDatabaseResponse:
    return await read_credit_cards_database(db=db, request=request)

@app.post("/compute_optimal_allocation")
async def compute_optimal_allocation_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], 
                   request: OptimalCardsAllocationRequest, db: Session = Depends(get_sync_db)) -> OptimalCardsAllocationResponse:
    print(request)
    return await optimize_credit_card_selection_milp(db=db, user=current_user, request=request)

@app.post("/read_user_held_cards")
async def read_user_held_cards_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)]) -> CreditCardsDatabaseResponse:
    user_cards = current_user.credit_cards
    user_cards_schemas = [CreditCardSchema.model_validate(cc) for cc in user_cards]
    return CreditCardsDatabaseResponse(credit_card=user_cards_schemas) 

@app.post("/read_user_preferences")
async def read_user_preferences_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], db: Session = Depends(get_sync_db)) -> PreferencesSchema:
    return teller_endpoints.read_user_preferences(user=current_user)

@app.post("/read_user_wallets")
async def read_user_wallets_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], db: Session = Depends(get_sync_db)) -> List[WalletSchema]:
    return teller_endpoints.read_user_wallets(user=current_user, db=db)

@app.post("/ingest_user_wallet")
async def ingest_user_wallet_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], 
                   wallet: WalletsIngestRequest, db: Session = Depends(get_sync_db)) -> WalletSchema:
    return teller_endpoints.ingest_user_wallet(wallet=wallet, user=current_user, db=db)

@app.post("/delete_user_wallet")
async def delete_user_wallet_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], 
                   wallet: WalletDeleteRequest, db: Session = Depends(get_sync_db)):
    return teller_endpoints.delete_wallet(request=wallet, current_user=current_user, db=db)

@app.post("/edit_user_wallet")
async def edit_user_wallet_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], 
                   wallet: WalletUpdateRequest, db: Session = Depends(get_sync_db)):
    return teller_endpoints.edit_wallet(request=wallet, current_user=current_user, db=db)

@app.get("/api/is_user_logged_in")
def is_user_logged_in(current_user: Annotated[User, Depends(auth_utils.get_current_user)]) -> dict:
    print(f"[INFO] {current_user.email} is logged in")
    return {"detail": "cardmath_user_authenticated"}

@app.post("/create_checkout_session")
def create_checkout_session_endpoint(request: CheckoutSessionRequest,
                                     current_user: User = Depends(auth_utils.get_current_user),
                                     db = Depends(get_sync_db)) -> CheckoutSessionResponse:
    return create_checkout_session(db=db, current_user=current_user, request=request)

@app.post("/get_checkout_session")
def get_checkout_session_endpoint(request: CheckoutSessionIDRequest): 
    return get_checkout_session(request=request)

@app.post("/stripe-webhook")
async def stripe_webhook_endpoint(request: Request , db: Session = Depends(get_sync_db)):
    return await stripe_webhook(request=request, db=db)

@app.post("/password-recovery-email")
async def request_password_recovery_endpoint(request: PasswordResetRequest, db: Session = Depends(get_sync_db)):
    return await request_password_recovery(email=request.email, db=db)

@app.post("/reset-password")
async def reset_password_endpoint(form_data: PasswordResetForm, db: Session = Depends(get_sync_db)):
    return await reset_password(token=form_data.token, new_password=form_data.new_password, db=db)

@app.post("/delete-user-data")
async def delete_user_data_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], db: Session = Depends(get_sync_db)):
    return auth_crud.delete_user_data(user=current_user, db=db)

@app.post("/process-onboarding-enrollment")
async def process_onboarding_complete_endpoint(teller_connect_response: AccessTokenSchema, answers: dict,  db: Session = Depends(get_sync_db)):
    return await create_onboarding_token(db=db, teller_connect_response=teller_connect_response, answers=answers) 

@app.post("/compute-onboarding-savings")
async def compute_onboarding_savings_endpoint( request: OnboardingSavingsRequest, db: Session = Depends(get_sync_db)):
    return await get_onboarding_recommendation(db=db, request=request)

@app.post("/chat")
async def chat_endpoint(request: ChatRequest) -> StreamingResponse:
    return await chat(request=request)

@app.get("/api/issuers")
def get_issuers():
    return [issuer.value for issuer in Issuer]

@app.get("/api/reward_units")
def get_reward_units():
    return [reward_unit.value for reward_unit in RewardUnit]

@app.get("/api/keywords")
def get_keywords():
    return [keyword.value for keyword in CreditCardKeyword]

@app.get("/api/grocery_stores")
def get_grocery_stores():
    return [vendor.value for vendor in Vendors if Vendors.get_category(vendor) == PurchaseCategory.GROCERIES]

@app.get("/api/general_goods_stores")
def get_general_goods_stores():
    return [vendor.value for vendor in Vendors if Vendors.get_category(vendor) == PurchaseCategory.SHOPPING]

@app.get("/api/lifestyles")
def get_lifestyles():
    return [lifestyle.value for lifestyle in Lifestyle]

@app.get("/api/industries")
def get_industries():
    return [industry.value for industry in IndustryType]

@app.get("/api/business_sizes")
def get_business_sizes():
    return [size.value for size in BusinessSize]