from database.auth.user import User, UserInDB
from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

UserModel = sqlalchemy_to_pydantic(User, exclude=['id'])
UserInDBModel = sqlalchemy_to_pydantic(UserInDB)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(UserModel):
    password: str

class UserUpdate(UserModel):
    password: str | None = None