from database.sql_alchemy_db import Base
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Index, CheckConstraint
from sqlalchemy.orm import relationship

class MockHeavyHitter(Base):
    __tablename__ = 'mock_heavy_hitters'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    onboarding_id = Column(Integer, ForeignKey('onboarding.id', ondelete='CASCADE'), nullable=True)
    
    # Store "VENDOR" or "CATEGORY" using our enum
    type = Column(String, nullable=False)
    
    name = Column(String, nullable=True)
    category = Column(String, nullable=False)
    percent = Column(String, nullable=False)
    amount = Column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint(
            '(user_id IS NOT NULL OR onboarding_id IS NOT NULL)',
            name='enrollment_owner_check'
        ),
    )

    user = relationship('User', backref='mock_heavyhitters', uselist=False)
    onboarding = relationship('Onboarding', backref='mock_heavyhitters', uselist=False)


class Transaction(Base):
    __tablename__ = 'transactions'
    
    txn_id = Column(String, primary_key=True, nullable=False)  # returned by teller
    
    account_id = Column(String, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False, index=True)
    account = relationship("Account", backref="transactions")
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False, index=True)
    description = Column(String, nullable=False)
    
    details = relationship(
        "TransactionDetails", 
        back_populates="transaction", 
        uselist=False, 
        cascade="all, delete-orphan"
    )

    status = Column(String, nullable=False)
    running_balance = Column(Float, nullable=True)
    type = Column(String, nullable=False)

    __table_args__ = (
        Index('ix_transactions_status', 'status', postgresql_using='btree'),
    )
        
class TransactionDetails(Base):
    __tablename__ = 'transaction_details'
    
    txn_id = Column(String, ForeignKey('transactions.txn_id', ondelete="CASCADE"), primary_key=True)
    counterparty_id = Column(Integer, ForeignKey('counterparty.id', ondelete="CASCADE"))
    processing_status = Column(String, nullable=False)
    category = Column(String, nullable=True)
    
    counterparty = relationship(
        "Counterparty", 
        back_populates="transaction_details", 
        cascade="all"
    )
    transaction = relationship("Transaction", back_populates="details", uselist=False)

    __table_args__ = (
        Index('ix_transaction_details_category', 'category', postgresql_using='btree'),
    )

class Counterparty(Base):
    __tablename__ = 'counterparty'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    type = Column(String, nullable=True)
    
    transaction_details = relationship(
        "TransactionDetails", 
        back_populates="counterparty", 
        uselist=True, 
        single_parent=True,
        cascade="all, delete-orphan"
    ) 
