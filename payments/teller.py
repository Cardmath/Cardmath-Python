from database.auth.user import Onboarding, Enrollment, Account, User, Subscription
from sqlalchemy.orm import Session, joinedload
from teller.utils import Teller
from fastapi import HTTPException
from teller.schemas import TellerPaymentsAPIRequest, Payee
from pydantic import BaseModel
from typing import List, Optional

class ZellePaymentInitiationRequest(BaseModel):
    acc_id: str

class ZellePaymentInitiationResponse(BaseModel):
    verified: bool
    teller_connect_token: Optional[str]
    
def initiate_zelle_payment(request: ZellePaymentInitiationRequest, onboarding: Onboarding):
    onb_enrollment: Enrollment = onboarding.enrollment
    onb_accs: List[Account] = onb_enrollment.accounts
    
    if not any(request.acc_id == aid for aid in map(lambda x: str(x.id), onb_accs)):
        raise HTTPException(status_code=401, detail="Account does not belong to user")
    
    payment = TellerPaymentsAPIRequest(amount="99.99")
    client = Teller()
    response: dict = client.initiate_subscription_zelle_payment(acc_id=request.acc_id, accessToken=onb_enrollment.access_token, payment=payment)
    print(f"TELLER RESPONDED: {response}")

    if response.get("connect_token"):
        return ZellePaymentInitiationResponse(verified=False, teller_connect_token=response.get("connect_token"))
    elif response.get("id") and verify_zelle_payment(request=ZellePaymentVerficationRequest(acc_id=request.acc_id, pid=response.get("id")), onboarding=onboarding):
        return ZellePaymentInitiationResponse(verified=True, teller_connect_token=None)

class ZellePaymentVerficationRequest(BaseModel):
    acc_id: str
    pid: str

def verify_zelle_payment(request: ZellePaymentVerficationRequest, onboarding: Onboarding):
    client = Teller()
    
    if not onboarding.user:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not onboarding.user.subscription:
        raise HTTPException(status_code=401, detail="Subscription not found")
    
    user_not_paid: bool = onboarding.user.subscription.status == "unverified"
    payment_verified: bool = client.validate_payment(acc_id=request.acc_id, pid=request.pid, accessToken=onboarding.enrollment.access_token)
    
    if not (user_not_paid and payment_verified):
        raise HTTPException(status_code=401, detail="Not able to verify the user's payment. Please contact support@cardmath.ai.")
    
    return True