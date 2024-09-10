from database import models
from database.crud import *
from database.sql_alchemy_db import SessionLocal, engine
from extract_utils import extract_cardratings
from fastapi import Depends, FastAPI
from schemas import *
from sqlalchemy.orm import Session
import json
import os
import requests

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
    
@app.post("/download")
def download(request : DownloadRequest, db: Session = Depends(get_db)):
    if os.path.exists(request.file_path) or not request.force_download:
        return "File already exists or download not forced."
    else:
        headers = {
            'User-Agent': request.user_agent
        }
        response = requests.get(request.fallback_url, headers=headers)
        with open(request.file_path, 'wb') as file:
            file.write(response.content)
        return f"File downloaded at {request.file_path}."

@app.post("/extract")
def extract(request : ExtractRequest) -> ExtractResponse:    
    cc_list = extract_cardratings(request.raw_html, request.max_items_to_extract)
    json_data = json.dumps(cc_list)
    
    if request.save_to_db:
        db = get_db()
        for cc in cc_list:
            create_cardratings_scrape(db, cc)
    
    return ExtractResponse(raw_json_out=json_data, db_log= [0, 1]) # PLACEHOLDER DB LOG
    

@app.post("/parse") 
def parse(request : ParseRequest) -> ParseResponse:
    unparsed_ccs : list = []        
    if (len(request.raw_json_in) > 0):
        unparsed_ccs = json.loads(request.raw_json_in)
    else :
        db = get_db()
        # TODO put a field in the parserequest for more granularity
        unparsed_ccs = get_all_cardratings_scrapes(db)
        
    out_parsed_cards : list = []
    if request.save_to_db:
        db = get_db()

    db_log = []  # Add db_log field

    for cc in unparsed_ccs:
        parsed_cc = CreditCardCreate(
            name=cc['name'],
            issuer=cc['issuer'], 
            score_needed=cc['score_needed'],
            description_used=cc['description_used'],
            card_attributes=cc['card_attributes']
            ).create()

        if request.save_to_db:
            db_log.append(create_credit_card(db, parsed_cc))
        
        if request.return_json:
            out_parsed_cards.append(parsed_cc.to_json())
    
    return ParseResponse(raw_json_out=out_parsed_cards, db_log=db_log)  # Remove json.dumps()
          
