from database.auth.user import Enrollment, Onboarding
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from datetime import timedelta
from insights.optimal_cards.endpoint import optimize_credit_card_selection_milp, OptimalCardsAllocationRequest, OptimalCardsAllocationResponse
from pydantic import BaseModel, EmailStr, ConfigDict
from requests import Response
from sqlalchemy.orm import Session
from teller.schemas import AccessTokenSchema
from typing import List, Tuple, Union
from uuid import uuid4
import json
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
    token = str(uuid4()) 
    expiration = datetime.now() + timedelta(minutes=30)
    enr_id = teller_connect_response.enrollment.id
    
    # Check if enrollment exists
    if db.query(Enrollment).filter(Enrollment.id == enr_id).first():
        raise ValueError(f"Enrollment ID {enr_id} already present in the database.")
    
    # Create onboarding first
    onboarding = Onboarding(
        token=token,
        created_at=datetime.now(),
        expires_at=expiration,
        is_used=False,
        phone_numbers=[],
        emails=[]
    )
    db.add(onboarding)
    db.flush()  # This gets us the onboarding ID
    
    # Now create enrollment with onboarding_id
    enrollment = Enrollment(
        id=enr_id,
        user_id=None,
        onboarding_id=onboarding.id,  # Set this explicitly
        access_token=teller_connect_response.accessToken,
        institution_name=teller_connect_response.enrollment.institution.name,
        signatures=teller_connect_response.signatures,
        last_updated=datetime.now()
    )
    db.add(enrollment)
    
    teller_client = teller_utils.Teller()
    identity = teller_client.fetch_identity(access_token=teller_connect_response.accessToken)
    
    contact_info: ContactInfo = extract_contact_info(identity)
    
    # Update onboarding with contact info
    onboarding.phone_numbers = contact_info.phone_numbers
    onboarding.emails = contact_info.emails
    
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
    print(f"Got onboarding and enrollment for token {request.token}")

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
    
    print(f"Created optimization request for token {request.token}")
    teller_client = teller_utils.Teller()
    
    # Optimize for onboarding by setting bulk_mode=True and using a larger batch size
    teller_client.fetch_enrollment_transactions(
        db=db, 
        enrollment=enrollment, 
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
