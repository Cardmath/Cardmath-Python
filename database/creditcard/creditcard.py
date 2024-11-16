from creditcard.enums import *
from database.sql_alchemy_db import Base
from sqlalchemy.orm import relationship
from database.auth.user import user_credit_card_association
from sqlalchemy import Column, String, Float, JSON, Integer 

# standard CreditCard object
class CreditCard(Base):
    __tablename__ = "credit_cards"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)  
    issuer = Column(String) # Issuer enum
    reward_category_map = Column(JSON) # Store mapping as json dumps
    benefits = Column(JSON) # Benefits enum in json array
    credit_needed = Column(JSON) # CreditNeeded enum in json array 
    sign_on_bonus = Column(JSON) # SignOnBonus enum in json array
    apr = Column(JSON) # APR enum in json array
    annual_fee = Column(JSON)
    statement_credit = Column(JSON)
    primary_reward_unit = Column(String) # RewardUnit enum
    keywords = Column(JSON) # Keywords enum in json array
    users = relationship("User", secondary=user_credit_card_association, back_populates="credit_cards")