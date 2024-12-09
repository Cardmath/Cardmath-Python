import json
from datetime import timedelta
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from uuid import uuid4
from datetime import datetime, timedelta
from database.auth.user import Enrollment, Onboarding, User
from teller.schemas import TransactionSchema 
from teller.schemas import AccessTokenSchema
from teller.schemas import AccountSchema
from pydantic import BaseModel, EmailStr, ConfigDict
from insights.optimal_cards.endpoint import optimize_credit_card_selection_milp, OptimalCardsAllocationRequest
from insights.schemas import MonthlyTimeframe
from typing import List, Tuple, Union
import teller.utils as teller_utils
from requests import Response

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
    token = str(uuid4()) 
    expiration = datetime.now() + timedelta(minutes=30)
    enr_id = teller_connect_response.enrollment.id
    
    enrollment = db.query(Enrollment).filter(Enrollment.id == enr_id).first()
    if enrollment:
        raise ValueError(f"Enrollment ID {enr_id} already present in the database.")
    else:
        enrollment = Enrollment(
            id=enr_id,
            user_id=None,
            access_token=teller_connect_response.accessToken,
            institution_name=teller_connect_response.enrollment.institution.name,
            signatures=teller_connect_response.signatures,
            last_updated=datetime.now()
        )
        db.add(enrollment)
    
    teller_client = teller_utils.Teller()
    identity = await teller_client.fetch_identity(access_token=teller_connect_response.accessToken)
    await teller_client.fetch_enrollment_transactions(db=db, enrollment=[teller_connect_response.enrollment], should_categorize=True)
    
    contact_info: ContactInfo = extract_contact_info(identity)
    
    onboarding = Onboarding(
        token=token,
        created_at=datetime.now(),
        expires_at=expiration,
        is_used=False,
        enrollment=enrollment,
        phone_numbers=contact_info.phone_numbers,
        emails=contact_info.emails
    )
    db.add(onboarding)
    db.commit()
    db.refresh(onboarding)
    
    return OnboardingCreationResponse(token=token, contact=contact_info, expires_at=expiration)

class OnboardingSavingsRequest(BaseModel):
    token: str
    answers: OnboardingQuestionsAnswers

class OnboardingSavingsResponse(BaseModel):
    total_savings: int
    regular_savings: int
    sign_on_bonus: int

    model_config = ConfigDict(from_attributes=True)  

def get_onboarding_token_enrollment(token: str, db: Session) -> Tuple[Onboarding, Enrollment]:
    onboarding: Onboarding = db.query(Onboarding).filter(Onboarding.token == token).first()
    if not onboarding:
        raise ValueError(f"No onboarding found for token {token}")

    enrollment: Enrollment = None
    if not onboarding.enrollment:
        print(f"Enrollment not found for onboarding of token {token}, falling back to enrollment_id")
        enrollment = db.query(Enrollment).filter(Enrollment.id == onboarding.enrollment_id).first()
    else :
        print(f"Enrollment found for onboarding of token {token}")
        enrollment = onboarding.enrollment

    if not enrollment:
        raise ValueError(f"No enrollment found for onboarding of token {token}")
    
    return onboarding, enrollment

async def get_onboarding_recommendation(request: OnboardingSavingsRequest, db: Session):
    # Get the onboarding and the enrollment
    onboarding, enrollment = get_onboarding_token_enrollment(request.token, db)

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

    optimization_result = await optimize_credit_card_selection_milp(
        db=db,
        user=onboarding,
        request=optimization_request
    )

    return optimization_result


