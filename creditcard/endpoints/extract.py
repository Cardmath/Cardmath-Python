import logging
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract(request: ExtractRequest, db: Session) -> ExtractResponse:
    """
    Extracts credit card ratings from raw HTML content or a file path.
    
    Parameters:
    - request (ExtractRequest): The request object containing raw HTML content and file path.
    - db (Session, optional): The database session.
    
    Returns:
    - ExtractResponse: The response object with extracted data in JSON format and database log.
    """
    
    # Read from file if raw HTML not provided
    if len(request.raw_html) == 0:
        logger.info(f"Reading HTML content from file: {request.file_path}")
        try:
            with open(request.file_path, "r") as f:
                request.raw_html = f.read()
            logger.info(f"File '{request.file_path}' read successfully, size: {len(request.raw_html)} bytes")
        except Exception as e:
            logger.error(f"Failed to read file: {request.file_path} - {e}")
            return ExtractResponse(db_log=[])

    logger.info("Extracting card information from HTML.")
    try:
        cc_list = extract_cardratings(request.raw_html, request.max_items_to_extract)
        logger.info(f"Extracted {len(cc_list)} cards.")
    except Exception as e:
        logger.error(f"Error during card extraction - {e}")
        return ExtractResponse(db_log=[])

    db_log = []
    if request.save_to_db:
        logger.info("Saving extracted cards to database.")
        for cc in cc_list:
            try:
                cc_created = cc.cardratings_scrape()
                crud.create_cardratings_scrape(db, cc_created)
                db_log.append(True)
                logger.info(f"Saved card '{cc.name}' to database.")
            except Exception as e:
                db_log.append(False)
                logger.error(f"Failed to save card '{cc.name}' to database - {e}")

    json_data = None
    if request.return_json:
        logger.info("Converting extracted data to JSON format.")
        try:
            json_data = json.dumps([cc.model_dump_json() for cc in cc_list])
            logger.info("Data successfully converted to JSON.")
        except Exception as e:
            logger.error(f"Failed to convert data to JSON - {e}")

    logger.info("Extraction process completed.")
    return ExtractResponse(raw_json_out=json_data, db_log=db_log)
