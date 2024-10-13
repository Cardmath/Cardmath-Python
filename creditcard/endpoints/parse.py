from creditcard.enums import *
from creditcard.schemas import CardRatingsScrapeSchema, CreditCardSchema
from creditcard.utils.parse import RewardCategoryRelation, RewardAmount
from database.creditcard import crud
from database.scrapes.cardratings import CardratingsScrape
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

import json

class ParseRequest(BaseModel):
    raw_json_in : str = None# list of json maps
    return_json: bool = True
    max_items_to_parse: int = 10
    save_to_db: bool = False
    
class ParseResponse(BaseModel):
    raw_json_out: Optional[List[str]] = None
    db_log : List[bool]

async def parse(request : ParseRequest, db : Session) -> ParseResponse:    
    extracted_ccs : List[CardRatingsScrapeSchema] = []
    if request.raw_json_in is not None and len(request.raw_json_in) > 0:
        json_in = json.loads(request.raw_json_in)
        extracted_ccs = [CardRatingsScrapeSchema.model_construct(cc) for cc in json_in]
    else :
        cc_scrapes : List[CardratingsScrape] = crud.read_cardratings_scrapes(db, n=request.max_items_to_parse)
        extracted_ccs = [CardRatingsScrapeSchema.model_validate(cc) for cc in cc_scrapes]

    parsed_ccs : List[CreditCardSchema] = []
    parsed_cc = None
    total_attempts = 0
    cc_schema_error_count = 0
    cc_orm_error_count = 0
    for extracted_cc in extracted_ccs:
        total_attempts += 1
        try:
            parsed_cc = await extracted_cc.credit_card_schema()
        except Exception as e:
            print("Error parsing: ", e)
            cc_schema_error_count += 1
            continue
        
        try :
            parsed_cc = parsed_cc.credit_card()
        except Exception as e:
            print("Error turning into credit card: ", e, parsed_cc)
            cc_orm_error_count += 1
            continue

        parsed_ccs.append(parsed_cc)
        

    db_log = []  # Add db_log field
    raw_json_out = None
    for parsed_cc in parsed_ccs:
        if request.save_to_db:
            db_result = crud.create_credit_card(db, parsed_cc)
            print(f"Inserted: {db_result}")
            db_log.append(db_result)

        if request.return_json:
            if raw_json_out is None:
                raw_json_out = []
            raw_json_out.append(parsed_cc.model_dump_json())

    print(f"Total attempts: {total_attempts}, cc_schema_error_count: {cc_schema_error_count}, cc_orm_error_count: {cc_orm_error_count}")
    return ParseResponse(raw_json_out=raw_json_out, db_log=[0,1])
          
