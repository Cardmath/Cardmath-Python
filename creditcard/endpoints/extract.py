from creditcard.enums import *
from creditcard.utils.extract import extract_cardratings
from database.creditcard import crud
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List

import json

class ExtractRequest(BaseModel):
    file_path : str = ""
    raw_html : str = "" 
    return_json: bool = True
    max_items_to_extract: int = 10
    save_to_db: bool = False
    
class ExtractResponse(BaseModel):
    raw_json_out: Optional[str] = None    
    db_log : List[bool]

def extract(request : ExtractRequest, db: Session) -> ExtractResponse:
    """
    Extracts credit card ratings from raw HTML content or a file path.
    Parameters:
    - request (ExtractRequest): The request object containing the raw HTML content and file path.
    - db (Session, optional): The database session. Defaults to the session obtained from get_db.
    Returns:
    - ExtractResponse: The response object containing the extracted credit card ratings in JSON format and a database log.
    """
    
    if len(request.raw_html) == 0 :
        with open(request.file_path, "r") as f:
            request.raw_html = f.read()    
    
    cc_list = extract_cardratings(request.raw_html, request.max_items_to_extract)
    if request.save_to_db:
        for cc in cc_list:
            cc_created = cc.cardratings_scrape()
            crud.create_cardratings_scrape(db, cc_created)
    
    json_data = None
    if request.return_json:
        json_data = json.dumps([cc.model_dump_json() for cc in cc_list])
            
    return ExtractResponse(raw_json_out=json_data, db_log= [0, 1]) # PLACEHOLDER DB LOG
    