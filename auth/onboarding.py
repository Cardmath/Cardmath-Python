from database.auth.user import Enrollment, Onboarding
from auth.schemas import UserCreate
import auth.utils as auth_utils
from database.auth.crud import create_user
from datetime import datetime, timedelta
from database.sql_alchemy_db import get_sync_db
from insights.optimal_cards.endpoint import optimize_credit_card_selection_milp, OptimalCardsAllocationRequest, OptimalCardsAllocationResponse
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, validate_email
from requests import Response
from sqlalchemy.orm import Session
from teller.schemas import AccessTokenSchema
from typing import List, Union
from fastapi import Depends
from typing import Annotated
import json
import jwt
import teller.utils as teller_utils

class ContactInfo(BaseModel):
    emails: List[EmailStr]
    phone_numbers: List[str]

    model_config = ConfigDict(from_attributes=True)

class OnboardingCreationResponse(BaseModel):
    token: str
    contact: ContactInfo

    model_config = ConfigDict(from_attributes=True)

class OnboardingQuestionsAnswers(BaseModel):
    num_cards:int
    credit_score:int

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
                # Extract emails
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

async def create_onboarding_token(db: Session, teller_connect_response: AccessTokenSchema, answers: dict) -> dict:
    onboarding_token_expires = timedelta(minutes=auth_utils.ONBOARDING_TOKEN_EXPIRE_MINUTES)
    onboarding_token = auth_utils.create_access_token(
        data={"teller_id": teller_connect_response.user.id}, expires_delta=onboarding_token_expires
    )
    expiration = datetime.now() + onboarding_token_expires
    enr_id = teller_connect_response.enrollment.id
    
    if db.query(Enrollment).filter(Enrollment.id == enr_id).first():
        raise ValueError(f"Enrollment ID {enr_id} already present in the database.")
    
    onboarding = Onboarding(
        teller_id = teller_connect_response.user.id,
        expires_at=expiration,
        phone_numbers=[],
        emails=[]
    )
    db.add(onboarding)
    db.flush()
    
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
    identity = teller_client.fetch_identity(access_token=teller_connect_response.accessToken)
    contact_info: ContactInfo = extract_contact_info(identity)
    
    onboarding.phone_numbers = contact_info.phone_numbers
    onboarding.emails = contact_info.emails
    
    db.commit()
    db.refresh(onboarding)
    
    return OnboardingCreationResponse(token=onboarding_token, contact=contact_info)

class OnboardingSavingsRequest(BaseModel):
    answers: OnboardingQuestionsAnswers

class OnboardingSavingsResponse(BaseModel):
    total_savings: int
    regular_savings: int
    sign_on_bonus: int

    model_config = ConfigDict(from_attributes=True)  

def get_current_onboarding(token: Annotated[str, Depends(auth_utils.oauth2_scheme)], db: Session = Depends(get_sync_db)):
    payload = jwt.decode(token, auth_utils.SECRET_KEY, algorithms=[auth_utils.ALGORITHM])
    teller_id: str = payload.get("teller_id")
    onboarding = db.query(Onboarding).where(Onboarding.teller_id == teller_id and Onboarding.expires_at > datetime.now()).first()
    
    if onboarding == None:
        raise ValueError("No unexpired Onboarding found with matching teller_id")
    
    return onboarding

async def get_onboarding_recommendation(request: OnboardingSavingsRequest, db: Session, onboarding: Annotated[Onboarding, Depends(get_current_onboarding)]):
    optimization_request = OptimalCardsAllocationRequest(
        to_use=request.answers.num_cards,
        to_add=2,
        timeframe=None,
        use_sign_on_bonus=True,
        return_cards_added=False,
        return_cards_used=False,
        return_cards_dropped=False,
        save_to_db=False,
    )
    
    teller_client = teller_utils.Teller()
    
    teller_client.fetch_enrollment_transactions(
        db=db, 
        enrollment=onboarding.enrollment, 
        should_categorize=False,
        bulk_mode=True,
        batch_size=200,  # Larger batch size for onboarding
        is_new_user=True  # Skip existence checks during onboarding
    )
    
    optimization_result: OptimalCardsAllocationResponse = await optimize_credit_card_selection_milp(
        db=db,
        user=onboarding,
        request=optimization_request
    )

    return optimization_result.solutions[0]

class IngestOnboardingPrimaryEmailRequest(BaseModel):
    first_name: str
    primary_email: str

    @field_validator('primary_email', mode='before')
    @classmethod
    def validate_primary_email(cls, v):
        name, email = validate_email(v)
        return email

def ingest_primary_email(request: IngestOnboardingPrimaryEmailRequest, onboarding: Onboarding, db: Session):
    create_user(db=db, onboarding=onboarding, primary_email=request.primary_email, first_name=request.first_name)