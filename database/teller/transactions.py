from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sql_alchemy_db import Base

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(String, primary_key=True)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    account_id = Column(String, nullable=False)
    account_link = Column(String, nullable=False)
    self_link = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    running_balance = Column(Float, nullable=True)
    
    details_id = Column(Integer, ForeignKey('transaction_details.id'), nullable=False)
    details = relationship("TransactionDetails", back_populates="transaction")

class TransactionDetails(Base):
    __tablename__ = 'transaction_details'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    processing_status = Column(String, nullable=False)
    category = Column(String, nullable=False)
    
    counterparty_id = Column(Integer, ForeignKey('counterparty.id'), nullable=False)
    counterparty = relationship("Counterparty", back_populates="transaction_details")
    
    transaction = relationship("Transaction", back_populates="details")

class Counterparty(Base):
    __tablename__ = 'counterparty'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    
    transaction_details = relationship("TransactionDetails", back_populates="counterparty")