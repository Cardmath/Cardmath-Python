from database.sql_alchemy_db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship

user_credit_card_association = Table(
    'user_credit_card_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('credit_card_id', Integer, ForeignKey('credit_cards.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    enrollments = relationship("Enrollment", back_populates="user")
    credit_cards = relationship("CreditCard", secondary=user_credit_card_association, back_populates="users")

class UserInDB(User):
    hashed_password = Column(String, nullable=False)
  
class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    access_token = Column(String, nullable=False)
    enrollment_id = Column(String, nullable=False)
    institution_name = Column(String, nullable=False)
    signatures = Column(JSON, nullable=False)
    user = relationship("User", back_populates="enrollments")
    
    accounts = relationship("Account", back_populates="enrollment")
    
class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(String, primary_key=True, index=True)  # Account ID from API Response
    enrollment_id = Column(String, ForeignKey('enrollments.enrollment_id'), nullable=False)
    institution_name = Column(String, nullable=False)
    institution_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    subtype = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    last_four = Column(String, nullable=False)
    status = Column(String, nullable=False)
    
    enrollment = relationship("Enrollment", back_populates="accounts")