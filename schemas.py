from database.models import CreditCard
from parse_utils import *
from pydantic import BaseModel
from typing import Tuple, List
import hashlib



# TODO move this into a config file
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0'

class CreditCardCreate(BaseModel):
    name : str
    issuer : str
    score_needed : str
    description_used : int
    card_attributes : str
    
    def create(self):
        name = self.name.replace('\u00AE', '')
        issuer = get_issuer(self.issuer)
        benefits = get_benefits(self.card_attributes)
        credit_needed = get_credit_needed(self.score_needed)
        reward_category_map = get_reward_category_map(self.card_attributes)
        apr = get_apr(self.card_attributes)
        id = hashlib.sha1((self.name + self.issuer + self.score_needed + str(self.description_used) + self.card_attributes).encode()).hexdigest()
        return CreditCard(name=name, 
                          issuer=issuer,
                          benefits=benefits,
                          credit_needed=credit_needed,
                          reward_category_map=reward_category_map,
                          apr=apr,
                          id=id)

class DownloadRequest(BaseModel):
    url: str
    file_path: str
    force_download: bool = False
    user_agent : str = USER_AGENT
    
class DownloadResponse(BaseModel):
    pass
    
class ExtractRequest(BaseModel):
    raw_html : str
    return_json: bool = True
    max_items_to_extract: int = 10
    save_to_db: bool = False
    
class ExtractResponse(BaseModel):
    raw_json_out: str = None    
    db_log : List[bool]

    
class ParseRequest(BaseModel):
    raw_json_in : str
    return_json: bool = True
    max_items_to_parse: int = 10
    save_to_db: bool = False
    
class ParseResponse(BaseModel):
    raw_json_out: List[str] = None
    db_log : List[bool]

