from .sql_alchemy_db import Base
from enums import *
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
import json

# standard CreditCard object
class CreditCard(Base):
    __tablename__ = "credit_cards"
    
    id = Column(String, primary_key=True) # Hex string representing the SHA1 hash of the CC object
    name = Column(String, nullable=False) 
    issuer = Column(String) # Issuer enum in json array
    reward_category_map = Column(String) # Store mapping as json dumps
    benefits = Column(String) # Benefits enum in json array
    credit_needed = Column(String) # CreditNeeded enum in json array 
    apr = Column(Float)
    
    def __str__(self):
        return (f"CreditCard(name={self.name}, issuer={self.issuer}, "
                f"rewards={self.reward_category_map}, "
                f"benefits={[benefit.value for benefit in self.benefits]}, "
                f"credit_needed={self.credit_needed})")
        
    def to_json(self):
        return json.dumps(
            {
                "name": self.name,
                "issuer": self.issuer,
                "reward_category_map": self.reward_category_map,
                "benefits": self.benefits,
                "credit_needed": self.credit_needed,
                "apr": self.apr
            }
        )