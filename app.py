from auth.schemas import Token
from auth.schemas import User, UserCreate
from contextlib import asynccontextmanager
from creditcard.endpoints.download import download
from creditcard.endpoints.download import DownloadRequest, DownloadResponse
from creditcard.endpoints.extract import extract
from creditcard.endpoints.extract import ExtractRequest, ExtractResponse
from creditcard.endpoints.parse import parse
from creditcard.endpoints.parse import ParseRequest, ParseResponse
from creditcard.schemas import *
from database.creditcard import creditcard
from database.sql_alchemy_db import engine, get_db, print_sql_schema
from database.sql_alchemy_db import SessionLocal
from datetime import timedelta
from fastapi import Request, Depends, FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from insights.heavyhitters import read_heavy_hitters
from insights.schemas import HeavyHittersRequest, HeavyHittersResponse
from sqlalchemy.orm import Session
from teller.schemas import AccessTokenSchema, PreferencesSchema
from typing import Annotated

import auth.utils as auth_utils
import database.auth.crud as auth_crud
import teller.endpoints as teller_endpoints

import logging

SAFE_LOCAL_DOWNLOAD_SPOT = "/home/johannes/CreditCards/cardratings/cardratings.html"

creditcard.Base.metadata.create_all(bind=engine)
#print_sql_schema() Only for debugging

@asynccontextmanager
async def lifespan(app: FastAPI):
    db : Session = SessionLocal()
    try :
        download(request=DownloadRequest(url = "https://www.cardratings.com/credit-card-list.html",
                file_path = SAFE_LOCAL_DOWNLOAD_SPOT,
                force_download = False,
                user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"))
    except Exception as e:
        print(e, "Error downloading cards!")
    
    try :
        extract(request=ExtractRequest(file_path=SAFE_LOCAL_DOWNLOAD_SPOT,
                return_json = False,
                max_items_to_extract = 10,
                save_to_db=True),
                db=db)
    except Exception as e:
        print(e, "Error extracting cards!")
    
    try :
        parse(request=ParseRequest(return_json = False,
            max_items_to_parse = 0,
            save_to_db=True),
            db = db)
    except Exception as e:
        print(e, "Error parsing cards - Probably an issue with OpenAI API connection")
    finally:
        db.close()
    
    yield

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
    db: Session = Depends(get_db)
) -> Token:
    """
    Authenticates a user and generates an access token.
    Parameters:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (Session, optional): The database session. Defaults to Depends(get_db).
    Returns:
        Token: The generated access token.
    Raises:
        HTTPException: If the username or password is incorrect.
    """
    
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
    db: Session = Depends(get_db)
) -> Token:
    """
    Register a user and generate an access token.
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the user's credentials.
        db (Session, optional): The database session. Defaults to Depends(get_db).
    Returns:
        Token: The generated access token.
    Raises:
        HTTPException: If the username is already taken.
    """

    if auth_crud.get_user_by_username(db, form_data.username) is not None:
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
    auth_crud.create_user(db, user)
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/process_new_enrollment")
async def process_new_enrollment(current_user: Annotated[User, Depends(auth_utils.get_current_user)],
                           db: Session = Depends(get_db)):
    return await teller_endpoints.process_new_enrollment(current_user, db)
    

@app.post("/receive_teller_enrollment")
async def receive_teller_enrollment(current_user: Annotated[User, Depends(auth_utils.get_current_user)],
                 access_token: AccessTokenSchema,
                 db: Session = Depends(get_db)):
    return await teller_endpoints.receive_teller_enrollment(db=db, access_token=access_token, user=current_user) 

@app.post("/ingest_user_preferences")
async def ingest_user_preferences(current_user: Annotated[User, Depends(auth_utils.get_current_user)],
                 preferences: PreferencesSchema,
                 db: Session = Depends(get_db)):
    return await teller_endpoints.ingest_user_preferences(preferences=preferences, db=db, user=current_user)

@app.post("/download")
def download_endpoint(request: DownloadRequest) -> DownloadResponse:
    return download(request)
    
@app.post("/extract")
def extract_endpoint(request: ExtractRequest, db: Session = Depends(get_db)) -> ExtractResponse:
    return extract(request, db)

@app.post("/parse") 
def parse_endpoint(request: ParseRequest, db: Session = Depends(get_db)) -> ParseResponse:
    return parse(request, db)

@app.post("/read_heavy_hitters") 
async def heavy_hitters_endpoint(current_user: Annotated[User, Depends(auth_utils.get_current_user)], 
                   request: HeavyHittersRequest, db: Session = Depends(get_db)) -> HeavyHittersResponse:
    return await read_heavy_hitters(db, current_user, request)
