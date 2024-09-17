from creditcard.enums import *
from creditcard.schemas import CreditCardCreate, ParseRequest, ParseResponse, CardRatingsScrapeSchema
from database import crud
from database.scrapes.cardratings import CardratingsScrape
from sqlalchemy.orm import Session
from typing import List
import json

def parse(request : ParseRequest, db : Session) -> ParseResponse:    
    parsed_ccs = []
    if request.raw_json_in is not None and len(request.raw_json_in) > 0:
        json_in = json.loads(request.raw_json_in)
        parsed_ccs = [CreditCardCreate.model_construct(cc) for cc in json_in]
    else :
        parsed_ccs : List[CardratingsScrape] = crud.get_cardratings_scrapes(db, n=request.max_items_to_parse)
        parsed_ccs : List[CardRatingsScrapeSchema] = [CardRatingsScrapeSchema(name=cc.name, 
                                                                              description_used=cc.description_used,
                                                                              unparsed_issuer=cc.unparsed_issuer,
                                                                              unparsed_credit_needed=cc.unparsed_credit_needed,
                                                                              unparsed_card_attributes = cc.unparsed_card_attributes) for cc in parsed_ccs]
        parsed_ccs : List[CreditCardCreate] = [cc.to_credit_card_create() for cc in parsed_ccs]
        
    out_parsed_cards : list = []
    db_log = []  # Add db_log field
    for parsed_cc in parsed_ccs:

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
          
