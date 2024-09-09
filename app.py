from fastapi import FastAPI
from pydantic import BaseModel
import os
import json
import requests
from extract_utils import extract_cardratings
from parse_utils import get_benefits, get_credit_needed, get_reward_category_map, get_issuer, get_apr

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0'

app = FastAPI()

class DownloadRequest(BaseModel):
    url: str
    file_path: str
    force_download: bool = False
    user_agent : str = USER_AGENT
    
@app.post("/download")
def download(request : DownloadRequest):
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

class ExtractRequest(BaseModel):
    file_path: str
    return_json: bool = True
    max_items_to_extract: int = 10

@app.post("/extract")
def extract(request : ExtractRequest):    
    cc_list = extract_cardratings(request.file_path, request.max_items_to_extract)
    json_data = json.dumps(cc_list)

    json_file_path = request.file_path.replace('.html', '.json')
    with open(json_file_path, 'w') as file:
        file.write(json_data)
    
    if (request.return_json):
        return (json_data, json_file_path)
    else : 
        return (None, json_file_path)
    

class ParseRequest(BaseModel):
    json_file_path: str
    raw_json_in : str
    return_json: bool = True
    max_items_to_parse: int = 10  

@app.post("/parse") 
def parse(request : ParseRequest):
    cc_list = []
    cc_parsed_list = []
    if (len(request.raw_json_in) > 0):
        cc_list = json.loads(request.raw_json_in)
    else :
        with open(request.json_file_path, 'r') as file:
            cc_list = json.load(file)
    
    for cc in cc_list: cc_parsed_list.append({"benefits" : get_benefits(cc['card_attributes']),
        "credit_needed" : get_credit_needed(cc['credit_needed']),
        "reward_category_map" : get_reward_category_map(cc['card_attributes']),
        "issuer" : get_issuer(cc['issuer']),
        "apr" : get_apr(cc['card_attributes'])
    })
    return json.dumps(cc_parsed_list)
    
          
