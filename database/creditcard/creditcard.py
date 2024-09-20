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
    apr = Column(Float)
    users = relationship("User", secondary=user_credit_card_association, back_populates="credit_cards")
    
    def __str__(self):
        return (f"CreditCard(name={self.name}, issuer={self.issuer}, "
                f"rewards={self.reward_category_map}, "
                f"benefits={[benefit.value for benefit in self.benefits]}, "
                f"credit_needed={self.credit_needed})")