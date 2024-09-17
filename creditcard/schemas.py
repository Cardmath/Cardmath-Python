from creditcard.utils.parse import *
from database.creditcard import CreditCard
from database.scrapes.cardratings import CardratingsScrape
from pydantic import BaseModel
from typing import List, Optional

# TODO move this into a config file
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0'

class CreditCardCreate(BaseModel):
    name : str = "No name"
    issuer : str = "No issuer"
    score_needed : str = "No score needed"
    description_used : int = 0
    card_attributes : str = "No card attributes"
    
    def create(self):
        name = self.name.replace('\u00AE', '')
        issuer = get_issuer(self.issuer)
        benefits = get_benefits(self.card_attributes)
        credit_needed = get_credit_needed(self.score_needed)
        reward_category_map = get_reward_category_map(self.card_attributes)
        apr = get_apr(self.card_attributes)
        return CreditCard(name=name, 
                          issuer=issuer,
                          benefits=benefits,
                          credit_needed=credit_needed,
                          reward_category_map=reward_category_map,
                          apr=apr)
        
class CardRatingsScrapeSchema(BaseModel):
    name: str
    description_used: int
    unparsed_issuer: str
    unparsed_credit_needed: str
    unparsed_card_attributes: str
    
    class Config:
        orm_mode = True
        from_attributes = True

    def create(self) -> CardratingsScrape:
        return CardratingsScrape(name=self.name,
                                 description_used=self.description_used,
                                 unparsed_issuer=self.unparsed_issuer,
                                 unparsed_credit_needed=self.unparsed_credit_needed,
                                 unparsed_card_attributes=self.unparsed_card_attributes)
        
    def to_credit_card_create(self) -> CreditCardCreate:
        return CreditCardCreate(name=self.name,
                                issuer=self.unparsed_issuer,
                                score_needed=self.unparsed_credit_needed,
                                description_used=self.description_used,
                                card_attributes=self.unparsed_card_attributes)
        
class CreditCardModel(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    reward_category_map: Optional[str] = None
    benefits: Optional[List[str]] = None
    credit_needed: Optional[List[str]] = None
    apr: Optional[float] = None

class DownloadRequest(BaseModel):
    url: str
    file_path: str
    force_download: bool = False
    user_agent : str = USER_AGENT
    
class DownloadResponse(BaseModel):
    status_code : str
    exists: bool = False # File already exists
    file_path : str = None # Path to downloaded file
    file_overwritten : bool = False # File was overwritten
    
class ExtractRequest(BaseModel):
    file_path : str = ""
    raw_html : str = "" 
    return_json: bool = True
    max_items_to_extract: int = 10
    save_to_db: bool = False
    
class ExtractResponse(BaseModel):
    raw_json_out: Optional[str] = None    
    db_log : List[bool]

    
class ParseRequest(BaseModel):
    raw_json_in : str = None# list of json maps
    return_json: bool = True
    max_items_to_parse: int = 10
    save_to_db: bool = False
    
class ParseResponse(BaseModel):
    raw_json_out: List[str] = None
    db_log : List[bool]

