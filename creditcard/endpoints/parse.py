from creditcard.enums import *
from creditcard.schemas import CreditCardCreate, ParseRequest, ParseResponse
from creditcard.utils.openai import prompt_gpt4_for_json, benefits_prompt, purchase_category_map_prompt, retry_openai_until_json_valid
from database import crud
from sqlalchemy.orm import Session
from typing import List
import json

def parse(request : ParseRequest, db : Session) -> ParseResponse:
    
    json_in = json.loads(request.raw_json_in)
    
    unparsed_ccs : List[dict] = []
    if len(json_in) > 0:
        for unparsed_cc in json_in:
            unparsed_ccs.append(unparsed_cc)
    else :
        unparsed_ccs = crud.get_all_cardratings_scrapes(db)
        
    out_parsed_cards : list = []
    db_log = []  # Add db_log field
    for cc in unparsed_ccs:
        parsed_cc = CreditCardCreate.model_construct(cc)

        if request.save_to_db:
            db_result = crud.create_credit_card(db, parsed_cc.create())
            db_log.append(db_result)
        
        if request.return_json:
            out_parsed_cards.append(parsed_cc.model_dump_json())
    
    mock_create = CreditCardCreate(
                name="Platinum Card",
                issuer="Chase",
                score_needed="Excellent",
                description_used=0,
                card_attributes="THIS IS A MOCK CARD") 
        
    if request.return_json:
        out_parsed_cards.append(mock_create.model_dump_json())
    if request.save_to_db:
        db_result = crud.create_credit_card(db, mock_create.create())

    return ParseResponse(raw_json_out=out_parsed_cards, db_log=db_log)
          
