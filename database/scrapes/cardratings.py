from database.sql_alchemy_db import Base
from sqlalchemy import Column, ForeignKey, Integer, String

class CardratingsScrape(Base):
    __tablename__ = "cardratings_scrape"

    scrape_id = Column(Integer, primary_key=True)
    credit_cards_id = Column(Integer, ForeignKey("credit_cards.id"), nullable=True)
    name = Column(String)
    description_used = Column(Integer)
    
    unparsed_issuer = Column(String)
    unparsed_credit_needed = Column(String)
    unparsed_card_attributes = Column(String) 
    
    def __str__(self) -> str:
        return (f"CardratingsScrape(name={self.name}, "
                f"description_used={self.description_used}, "
                f"unparsed_issuer={self.unparsed_issuer}, "
                f"unparsed_credit_needed={self.unparsed_credit_needed}, "
                f"unparsed_card_attributes={self.unparsed_card_attributes})")

# Potentially some other site scrapes such as Nerdwallet