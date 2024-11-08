from database.auth.user import User, UserInDB
from pydantic import BaseModel
from teller.schemas import AccessTokenSchema
from typing import Optional

class UserSchema(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: bool

class UserInDBSchema(UserSchema):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(UserSchema):
    password: str

class UserUpdate(UserSchema):
    password: Optional[str] = None