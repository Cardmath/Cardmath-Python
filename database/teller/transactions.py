from database.sql_alchemy_db import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

class Transaction(Base):
    __tablename__ = 'transactions'
    
    txn_id = Column(String, primary_key= True, nullable=False) # returned by teller
    
    account_id = Column(String, ForeignKey("accounts.id"), nullable=False, index=True) # account_id from teller
    account = relationship("Account", back_populates="transactions")
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String, nullable=False)
    
    details = relationship("TransactionDetails", back_populates="transaction", uselist=False)
    
    status = Column(String, nullable=False)
    running_balance = Column(Float, nullable=True)
    type = Column(String, nullable=False)

        
class TransactionDetails(Base):
    __tablename__ = 'transaction_details'
    
    txn_id = Column(String, ForeignKey('transactions.txn_id'), primary_key=True)
    counterparty_id = Column(Integer, ForeignKey('counterparty.id'))
    processing_status = Column(String, nullable=False)
    category = Column(String, nullable=True)
    
    counterparty = relationship("Counterparty", back_populates="transaction_details")
    transaction = relationship("Transaction", back_populates="details", uselist=False)

class Counterparty(Base):
    __tablename__ = 'counterparty'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    
    transaction_details = relationship("TransactionDetails", back_populates="counterparty", uselist=True) 