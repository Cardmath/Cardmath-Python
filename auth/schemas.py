from pydantic import BaseModel, ConfigDict
from typing import Optional
from creditcard.enums import CreditNeeded, IncomeRange
from creditcard.enums import Archetype

class UserSchema(BaseModel):
    teller_id: str
    email: str
    first_name: Optional[str] = None
    disabled: bool = False

class UserInDBSchema(UserSchema):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(UserSchema):
    password: Optional[str]

class UserUpdate(UserSchema):
    password: Optional[str] = None

class UserOnboarding(BaseModel):
    name: str
    archetype: Archetype
    wallet_size: int
    income: IncomeRange
    credit_score: CreditNeeded
    user_bio: str

    model_config = ConfigDict(extra='ignore')
