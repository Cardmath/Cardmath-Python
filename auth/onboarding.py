from database.auth.user import Enrollment, Onboarding, User 
from auth.schemas import UserOnboarding
import auth.utils as auth_utils
from database.auth.crud import create_user
from datetime import datetime, timedelta
from database.sql_alchemy_db import get_sync_db
from insights.heavyhitters import get_mock_heavy_hitters_response
from insights.optimal_cards.endpoint import optimize_credit_card_selection_milp, OptimalCardsAllocationRequest, OptimalCardsAllocationResponse
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, validate_email
from requests import Response
from auth.recovery import request_password_recovery
from sqlalchemy.orm import Session
from teller.mock import generate_and_save_heavy_hitters
from sqlalchemy import func
from database.auth.crud import get_user_by_email
from teller.schemas import AccessTokenSchema
from auth.schemas import Token
from typing import List, Union
from fastapi import Depends, HTTPException, status
from typing import Annotated, Optional, Dict

import json
import jwt
import teller.utils as teller_utils

class ContactInfo(BaseModel):
    emails: List[EmailStr] = []
    phone_numbers: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class OnboardingCreationResponse(BaseModel):
    token: str
    contact: Optional[ContactInfo]
    accounts: Dict

    model_config = ConfigDict(from_attributes=True)

class OnboardingQuestionsAnswers(BaseModel):
    num_cards: int
    use_mock: bool = False
    credit_score: int

def extract_contact_info(identity_response: Union[Response, dict]) -> ContactInfo:
    try:
        if isinstance(identity_response, Response):
            identity_data = identity_response.json()
        else:
            identity_data = identity_response
            
        # Ensure we're working with a list
        if not isinstance(identity_data, list):
            identity_data = [identity_data]
        
        all_emails = set()
        all_phone_numbers = set()
        
        for account in identity_data:
            owners = account.get('owners', [])
            for owner in owners:
                emails = owner.get('emails', [])
                for email in emails:
                    if email_data := email.get('data'):
                        all_emails.add(email_data)
                
                # Extract phone numbers
                phone_numbers = owner.get('phone_numbers', [])
                for phone in phone_numbers:
                    if phone_data := phone.get('data'):
                        all_phone_numbers.add(phone_data)
        
        return ContactInfo(
            emails=list(all_emails),
            phone_numbers=list(all_phone_numbers)
        )
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode identity response: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing identity response: {str(e)}")
    
def populate_onboarding_teller(db: Session, onboarding: Onboarding, teller_connect_response: AccessTokenSchema):
    enr_id = teller_connect_response.enrollment.id
    if db.query(Enrollment).filter(Enrollment.id == enr_id).first():
        raise ValueError(f"Enrollment ID {enr_id} already present in the database.")
    
    enrollment = Enrollment(
        id=enr_id,
        user_id=None,
        onboarding_id=onboarding.id,
        access_token=teller_connect_response.accessToken,
        institution_name=teller_connect_response.enrollment.institution.name,
        signatures=teller_connect_response.signatures,
        last_updated=datetime.now()
    )
    db.add(enrollment)

    teller_client = teller_utils.Teller()
    payment_accounts = teller_client.get_enrollment_zelle_accounts(enrollment=enrollment, db=db)

    identity = teller_client.fetch_identity(access_token=teller_connect_response.accessToken)
    contact_info: ContactInfo = extract_contact_info(identity)

    return payment_accounts, contact_info

def create_onboarding_token(db: Session, teller_connect_response: Optional[AccessTokenSchema], answers: UserOnboarding) -> dict:
    
    onboarding_token_expires = timedelta(minutes=auth_utils.ONBOARDING_TOKEN_EXPIRE_MINUTES)
    expiration = datetime.now() + onboarding_token_expires
    onboarding = Onboarding(
        archetype=answers.archetype,
        expires_at=expiration,
        phone_numbers=[],
        emails=[]
    )

    db.add(onboarding)
    db.flush()

    onboarding_token = auth_utils.create_access_token(
        data={"onboarding_id": onboarding.id}, expires_delta=onboarding_token_expires
    )
    
    payment_accounts=[]
    contact_info=ContactInfo()
    if teller_connect_response:
        print("teller connect response path")
        populate_onboarding_teller(db=db, onboarding=onboarding, teller_connect_response=teller_connect_response)
    elif answers.user_bio:
        print("heavy hitters path")
        generate_and_save_heavy_hitters(db=db, onboarding_id=onboarding.id, user_bio=answers.user_bio)

    return OnboardingCreationResponse(token=onboarding_token, contact=contact_info, accounts={acc.id: acc.name for acc in payment_accounts})

class OnboardingSavingsRequest(BaseModel):
    answers: OnboardingQuestionsAnswers

class OnboardingSavingsResponse(BaseModel):
    total_savings: int
    regular_savings: int
    sign_on_bonus: int

    model_config = ConfigDict(from_attributes=True)  

def get_current_onboarding(token: Annotated[str, Depends(auth_utils.oauth2_scheme)], db: Session = Depends(get_sync_db)):
    payload = jwt.decode(token, auth_utils.SECRET_KEY, algorithms=[auth_utils.ALGORITHM])
    onboarding_id: str = payload.get("onboarding_id")
    print("got the new onboarding id")
    onboarding = db.query(Onboarding).where(Onboarding.id == onboarding_id and Onboarding.expires_at > datetime.now()).first()
    
    if onboarding == None:
        raise HTTPException(status_code=401, detail="No unexpired Onboarding found with matching id")
    
    return onboarding

async def get_onboarding_recommendation(request: OnboardingSavingsRequest, db: Session, onboarding: Annotated[Onboarding, Depends(get_current_onboarding)]):
    override = None
    if request.answers.use_mock:
        override = get_mock_heavy_hitters_response(db=db, onboarding_id=onboarding.id)
    else:
        teller_client = teller_utils.Teller()
        
        teller_client.fetch_enrollment_transactions(
            db=db, 
            enrollment=onboarding.enrollment, 
            should_categorize=False,
            bulk_mode=True,
            batch_size=200,  # Larger batch size for onboarding
            is_new_user=True  # Skip existence checks during onboarding
        )

    optimization_request = OptimalCardsAllocationRequest(
        to_use=request.answers.num_cards,
        to_add=2,
        heavy_hitters_response_override=override,
        timeframe=None,
        use_sign_on_bonus=False,
        return_cards_added=False,
        return_cards_used=False,
        return_cards_dropped=False,
        save_to_db=False,
    )
    
    optimization_result: OptimalCardsAllocationResponse = await optimize_credit_card_selection_milp(
        db=db,
        user=onboarding,
        request=optimization_request,
    )

    return optimization_result

class IngestOnboardingPrimaryEmailRequest(BaseModel):
    first_name: str
    primary_email: str

    @field_validator('primary_email', mode='before')
    @classmethod
    def validate_primary_email(cls, v):
        name, email = validate_email(v)
        return email


def ingest_primary_email(request: IngestOnboardingPrimaryEmailRequest, onboarding: Onboarding, db: Session):
    if get_user_by_email(db, request.primary_email) is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,           
            detail="Username is already taken",
            headers={"WWW-Authenticate": "Bearer"},
        )
    create_user(db=db, onboarding=onboarding, primary_email=request.primary_email, first_name=request.first_name)
    request_password_recovery(email=request.primary_email, db=db)

def get_onboarding_user_token(onboarding: Onboarding):
    user: User = onboarding.user
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")