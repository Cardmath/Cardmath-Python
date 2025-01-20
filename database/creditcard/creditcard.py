from creditcard.enums import *
from database.sql_alchemy_db import Base
from sqlalchemy.orm import relationship
from database.auth.user import user_credit_card_association
from enum import Enum
from sqlalchemy import Column, TEXT, ForeignKey, ForeignKeyConstraint, DATE
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

class CreditCard(Base):
    __tablename__ = "credit_cards"
    
    # Keys, Immutable
    name = Column(TEXT, primary_key=True)
    issuer = Column(TEXT, primary_key=True)
    network = Column(TEXT, primary_key=True)
    key = Column(TEXT, ForeignKey("credit_cards_source.key"), nullable=True)
    
    # Only Modifiable Through Human Input
    referral_link = Column(TEXT, nullable=True)
    last_verified = Column(DATE, nullable=True)
    user_feedback = Column(ARRAY(TEXT), nullable=False, default=lambda: [])


    #Populated by OpenAI Structured Outputs

    # Complex Logic-Heavy Objects
    reward_category_map = Column(JSONB)      
    primary_reward_unit = Column(TEXT)

    sign_on_bonus = Column(JSONB)
    annual_fee = Column(JSONB)
    statement_credit = Column(JSONB)

    # JSON Arrays 
    benefits = Column(JSONB)
    apr = Column(JSONB)
    credit_needed = Column(JSONB) 
    keywords = Column(JSONB)

    users = relationship("User", secondary=user_credit_card_association, back_populates="credit_cards")
    
    __table_args__ = (
        ForeignKeyConstraint(
            ['name', 'issuer', 'network'],
            ['credit_cards_source.name', 'credit_cards_source.issuer', 'credit_cards_source.network'],
        ),
    )