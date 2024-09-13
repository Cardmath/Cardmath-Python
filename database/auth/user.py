from database.sql_alchemy_db import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)

class UserInDB(User):
    hashed_password = Column(String, nullable=False)