from database.auth.user import User, UserInDB
from pydantic import BaseModel

class UserSchema(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool

class UserInDBSchema(UserSchema):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(UserSchema):
    password: str

class UserUpdate(UserSchema):
    password: str | None = None