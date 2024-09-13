from auth.schemas import Token
from auth.schemas import User, UserInDB, UserCreate
from auth.utils import oauth2_scheme
from database import creditcard
from database.sql_alchemy_db import engine, get_db
from datetime import timedelta
from download_utils import download_html
from extract_utils import extract_cardratings
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import *
from sqlalchemy.orm import Session
from typing import Annotated
import auth.utils as auth_utils
import database.auth.crud as auth_crud
import database.crud as crud
import json
import os

creditcard.Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user = auth_utils.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,           
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/register")
async def register_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    if auth_crud.get_user_by_username(db, form_data.username) is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,           
            detail="Username is already taken",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = auth_utils.get_password_hash(form_data.password)
    user = UserCreate(username=form_data.username, 
                email=form_data.username, 
                full_name=form_data.username,
                disabled=False,
                password=form_data.password)
    auth_crud.create_user(db, user)
    access_token_expires = timedelta(minutes=auth_utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_utils.create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(auth_utils.get_current_user)]):
    return current_user

@app.get("/transactions/")
async def transactions(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

    
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
        parsed_cc = CreditCardCreate.model_construct(cc).create()

        if request.save_to_db:
            db_result = crud.create_credit_card(db, parsed_cc)
            db_log.append(db_result)
        
        if request.return_json:
            out_parsed_cards.append(parsed_cc.to_json())
    
    return ParseResponse(raw_json_out=out_parsed_cards, db_log=db_log)  # Remove json.dumps()
          
