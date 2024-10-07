from creditcard.enums import *
from creditcard.schemas import CardRatingsScrapeSchema, CreditCardSchema
from creditcard.utils.parse import RewardCategoryRelation, RewardAmount
from database.creditcard import crud
from database.scrapes.cardratings import CardratingsScrape
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

import json

class ParseRequest(BaseModel):
    raw_json_in : str = None# list of json maps
    return_json: bool = True
    max_items_to_parse: int = 10
    save_to_db: bool = False
    
class ParseResponse(BaseModel):
    raw_json_out: List[str] = None
    db_log : List[bool]

def parse(request : ParseRequest, db : Session) -> ParseResponse:    
    parsed_ccs = []
    if request.raw_json_in is not None and len(request.raw_json_in) > 0:
        print("[INFO] Parsing raw json")
        json_in = json.loads(request.raw_json_in)
        parsed_ccs = [CardRatingsScrapeSchema.model_construct(cc) for cc in json_in]
    else :
        print("[INFO] Parsing scraped data")
        cc_scrapes : List[CardratingsScrape] = crud.get_cardratings_scrapes(db, n=request.max_items_to_parse)
        print(f"[INFO] Fetched {len(cc_scrapes)} card ratings scrapes")
        cc_scrapes_schemas : List[CardRatingsScrapeSchema] = [CardRatingsScrapeSchema(name=cc.name, 
                                                                              description_used=cc.description_used,
                                                                              unparsed_issuer=cc.unparsed_issuer,
                                                                              unparsed_credit_needed=cc.unparsed_credit_needed,
                                                                              unparsed_card_attributes = cc.unparsed_card_attributes) for cc in cc_scrapes]
        print(f"[INFO] Constructed {len(cc_scrapes_schemas)} card ratings scrape schemas")  
        parsed_ccs : List[CreditCardSchema] = [cc.credit_card_schema() for cc in cc_scrapes_schemas]
        
    out_parsed_cards : list = []
    db_log = []  # Add db_log field
    for parsed_cc in parsed_ccs:

        if request.save_to_db:
            db_result = crud.create_credit_card(db, parsed_cc.credit_card())
            db_log.append(db_result)

        if request.return_json:
            out_parsed_cards.append(parsed_cc.model_dump_json())

    # START create a mock card
    
    mock_create = CreditCardSchema(
                name="Platinum Card",
                issuer=Issuer.CHASE,
                credit_needed=[CreditNeeded.EXCELLENT],
                reward_category_map= [RewardCategoryRelation(category=PurchaseCategory.TRAVEL, reward=RewardAmount(reward_unit=RewardUnit.CITI_THANKYOU_POINTS, amount=3))],
                benefits=[Benefit.AIRPORT_LOUNGE_ACCESS],
                apr = 0.5) 

    if request.return_json:
        out_parsed_cards.append(mock_create.model_dump_json())
    if request.save_to_db:
        db_result = crud.create_credit_card(db, mock_create.credit_card())
    
    # END create a mock card

    return ParseResponse(raw_json_out=out_parsed_cards, db_log=db_log)
          
