from pydantic import BaseModel
from typing import Optional

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