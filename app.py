from database import models
import database.crud as crud
from database.sql_alchemy_db import SessionLocal, engine
from download_utils import download_html
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
    
# Download a website locally
@app.post("/download")
def download(request: DownloadRequest) -> DownloadResponse:
    file_path = request.file_path
    exists = os.path.exists(file_path)
    file_overwritten = False
    status_code = "No Status Code"
    
    if exists and not request.force_download:
        status_code = "200"
    elif not exists or request.force_download:
        file_path, status_code = download_html(user_agent=request.user_agent,
                                               url=request.url,
                                               file_path=file_path)
        file_overwritten = exists

    return DownloadResponse(
        status_code=status_code,
        file_path=file_path,
        file_overwritten=file_overwritten)
    
@app.post("/extract")
def extract(request : ExtractRequest, db: Session = Depends(get_db)) -> ExtractResponse:
    if len(request.raw_html) == 0 :
        with open(request.file_path, "r") as f:
            request.raw_html = f.read()    
    
    cc_list = extract_cardratings(request.raw_html, request.max_items_to_extract)
    json_data = json.dumps(cc_list)
    
    if request.save_to_db:
        for cc in cc_list:
            crud.create_cardratings_scrape(db, cc)
    
    return ExtractResponse(raw_json_out=json_data, db_log= [0, 1]) # PLACEHOLDER DB LOG
    

@app.post("/parse") 
def parse(request : ParseRequest, db: Session = Depends(get_db)) -> ParseResponse:
    unparsed_ccs : list = []        
    if len(request.raw_json_in) > 0:
        unparsed_ccs = json.loads(request.raw_json_in)
    else :
        unparsed_ccs = crud.get_all_cardratings_scrapes(db)
        
    out_parsed_cards : list = []
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
            db_result = crud.create_credit_card(db, parsed_cc)
            db_log.append(db_result)
        
        if request.return_json:
            out_parsed_cards.append(parsed_cc.to_json())
    
    return ParseResponse(raw_json_out=out_parsed_cards, db_log=db_log)  # Remove json.dumps()
          
