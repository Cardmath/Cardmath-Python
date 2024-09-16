from database.sql_alchemy_db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float

class CardratingsScrape(Base):
    __tablename__ = "cardratings_scrape"

    scrape_id = Column(Integer, primary_key=True)
    credit_cards_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=True)
    name = Column(String)
    description_used = Column(Integer)
    
    unparsed_issuer = Column(String)
    unparsed_credit_needed = Column(String)
    unparsed_card_attributes = Column(String) 

# Potentially some other site scrapes such as Nerdwallet