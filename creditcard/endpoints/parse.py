import logging
import json
import pickle
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from creditcard.schemas import CardRatingsScrapeSchema
from creditcard.utils.extract import extract_cardratings
from database.creditcard import crud

# Set up logging
logger = logging.getLogger(__name__)

class ParseRequest(BaseModel):
    raw_json_in: Optional[str] = None
    max_items_to_parse: int = 10
    save_to_db: bool = False
    return_json: bool = True
    from_pkl: bool = False
    pkl_file_path: Optional[str] = None

class ParseResponse(BaseModel):
    raw_json_out: Optional[List[str]] = None
    db_log: List[int]

async def parse(request: ParseRequest, db: Session) -> ParseResponse:
    extracted_ccs: List[CardRatingsScrapeSchema] = []

    if request.from_pkl and request.pkl_file_path:
        # Load card data from pickle file
        logger.info(f"Loading card data from pickle file: {request.pkl_file_path}")
        try:
            extracted_ccs = from_pkl(request.pkl_file_path)
            logger.info(f"Loaded {len(extracted_ccs)} cards from pickle file.")
        except Exception as e:
            logger.error(f"Failed to load from pickle file: {e}")
            return ParseResponse(db_log=[])
    elif request.raw_json_in:
        # Parse from raw JSON input
        logger.info("Parsing raw JSON input")
        json_in = json.loads(request.raw_json_in)
        extracted_ccs = [CardRatingsScrapeSchema.model_construct(cc) for cc in json_in]
    else:
        # Read card ratings scrapes from the database
        logger.info("Reading card ratings scrapes from database")
        cc_scrapes = crud.read_cardratings_scrapes(db, n=request.max_items_to_parse)
        extracted_ccs = [CardRatingsScrapeSchema.model_validate(cc) for cc in cc_scrapes]

    raw_json_out = None
    total_attempts = 0
    cc_schema_error_count = 0
    cc_orm_error_count = 0

    for extracted_cc in extracted_ccs:
        total_attempts += 1
        try:
            parsed_cc = await extracted_cc.credit_card_schema()
            logger.info(f"Successfully parsed credit card schema for card: {parsed_cc}")
        except Exception as e:
            logger.error(f"Error parsing credit card from scrape: {e}")
            cc_schema_error_count += 1
            continue
        
        try:
            parsed_cc = parsed_cc.credit_card()
            logger.info(f"Credit card object created: {parsed_cc}")
        except Exception as e:
            logger.error(f"Error turning into credit card: {e}")
            cc_orm_error_count += 1
            continue

        if request.save_to_db:
            db_result = crud.create_credit_card(db, parsed_cc)
            logger.info(f"Inserted credit card into database: {db_result}")

        if request.return_json:
            if raw_json_out is None:
                raw_json_out = []
            raw_json_out.append(parsed_cc.model_dump_json())
        
    logger.info(f"Total attempts: {total_attempts}, Schema errors: {cc_schema_error_count}, ORM errors: {cc_orm_error_count}")
    return ParseResponse(raw_json_out=raw_json_out, db_log=[cc_schema_error_count, cc_orm_error_count])

def from_pkl(file_path: str) -> List[CardRatingsScrapeSchema]:
    """
    Load a list of CardRatingsScrapeSchema objects from a pickle file.
    
    Parameters:
    - file_path (str): Path to the pickle file containing card data.
    
    Returns:
    - List[CardRatingsScrapeSchema]: A list of instantiated CardRatingsScrapeSchema objects.
    """
    card_list = []
    
    with open(file_path, 'rb') as file:
        card_data = pickle.load(file)
    
    for card_name, card_info in card_data.items():
        card_instance = CardRatingsScrapeSchema(
            name=card_info['name'],
            description_used=0,  # Adjust this as per actual data
            unparsed_issuer=card_info['unparsed_issuer'],
            unparsed_credit_needed=card_info['unparsed_credit_needed'],
            unparsed_card_attributes=card_info['unparsed_card_attributes']
        )
        card_list.append(card_instance)
    
    return card_list
