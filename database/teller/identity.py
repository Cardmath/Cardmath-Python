from database.sql_alchemy_db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    last_four = Column(String, nullable=False)
    type = Column(String, nullable=False)
    enrollment_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    self_link = Column(String, nullable=False)
    transactions_link = Column(String, nullable=False)
    balances_link = Column(String, nullable=False)
    details_link = Column(String, nullable=False)
    institution_id = Column(String, nullable=False)
    institution_name = Column(String, nullable=False)
    subtype = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    
    owners = relationship("Owner", back_populates="account")

class Owner(Base):
    __tablename__ = 'owners'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(String, ForeignKey('accounts.id'), nullable=False)
    type = Column(String, nullable=False)
    
    account = relationship("Account", back_populates="owners")
    addresses = relationship("Address", back_populates="owner")
    names = relationship("Name", back_populates="owner")
    phone_numbers = relationship("PhoneNumber", back_populates="owner")
    emails = relationship("Email", back_populates="owner")

class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)
    primary = Column(Boolean, nullable=False)
    postal_code = Column(String, nullable=False)
    street = Column(String, nullable=False)
    region = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    
    owner = relationship("Owner", back_populates="addresses")

class Name(Base):
    __tablename__ = 'names'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)
    data = Column(String, nullable=False)
    type = Column(String, nullable=False)
    
    owner = relationship("Owner", back_populates="names")

class PhoneNumber(Base):
    __tablename__ = 'phone_numbers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)
    data = Column(String, nullable=False)
    type = Column(String, nullable=False)
    
    owner = relationship("Owner", back_populates="phone_numbers")

class Email(Base):
    __tablename__ = 'emails'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)
    data = Column(String, nullable=False)
    
    owner = relationship("Owner", back_populates="emails")