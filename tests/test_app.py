from app import app, parse, ParseRequest, ParseResponse, ExtractRequest, DownloadRequest
from download_utils import remove_if_exists
from fastapi.testclient import TestClient
import json
import os
import pytest

client = TestClient(app)

SAFE_LOCAL_DOWNLOAD_SPOT = "/home/johannes/CreditCards/cardratings.html"

def test_end_to_end():
    
    remove_if_exists(SAFE_LOCAL_DOWNLOAD_SPOT)
    assert not os.path.exists(SAFE_LOCAL_DOWNLOAD_SPOT)
    
    download_request = DownloadRequest(
        url = "https://www.cardratings.com/credit-card-list.html",
        file_path = SAFE_LOCAL_DOWNLOAD_SPOT,
        force_download = True,
        user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"
    )
    download_response = client.post("/download", content=download_request.model_dump_json())
    
    print("[End-to-End Test] Download Request Sent")
    assert download_response.status_code == 200
    download_path = json.loads(download_response.content.decode("utf-8"))["file_path"]
    print("[End-to-End Test] Download Response Received")
    assert download_path == SAFE_LOCAL_DOWNLOAD_SPOT
    print("[End-to-End Test] Downloaded Response Processed")

    extract_request = ExtractRequest(
        file_path=SAFE_LOCAL_DOWNLOAD_SPOT,
        return_json = True,
        max_items_to_extract = 1,
        save_to_db = False
    )
    
    print("[End-to-End Test] Extract Request Sent")
    extract_response = client.post("/extract", content=extract_request.model_dump_json()) 
    assert extract_response.status_code == 200
    print("[End-to-End Test] Extract Response Received")
    raw_json_in = json.loads(extract_response.content.decode("utf-8"))["raw_json_out"]
    print("[End-to-End Test] Extract Response Processed")
    
    parse_request_with_raw = ParseRequest(
        raw_json_in = raw_json_in,
        return_json = True,
        max_items_to_parse = 1,
        save_to_db = False
    )
    parse_response_with_raw = client.post("/parse", content=parse_request_with_raw.model_dump_json())
    print("[End-to-End Test] Parse Request Sent")
    assert parse_response_with_raw.status_code == 200
    print("[End-to-End Test] Parse Response Received")
    raw_json_out = json.loads(parse_response_with_raw.content.decode("utf-8"))["raw_json_out"]
    assert len(json.loads(raw_json_out[0])["name"]) > 0
    print("[End-to-End Test] Parse Response Processed")
    print("Successful End-to-End Test")
    

def test_download():
    remove_if_exists(SAFE_LOCAL_DOWNLOAD_SPOT)
    assert not os.path.exists(SAFE_LOCAL_DOWNLOAD_SPOT)

    request_data = DownloadRequest(
        url = "https://www.cardratings.com/credit-card-list.html",
        file_path = SAFE_LOCAL_DOWNLOAD_SPOT,
        force_download = True,
        user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0"
    )
    response = client.post("/download", content=request_data.model_dump_json())
    
    assert response.status_code == 200
    assert os.path.exists(SAFE_LOCAL_DOWNLOAD_SPOT)
    remove_if_exists(SAFE_LOCAL_DOWNLOAD_SPOT)
    assert not os.path.exists(SAFE_LOCAL_DOWNLOAD_SPOT)

def test_parse_with_raw_json():
    request_data = json.dumps({
        "raw_json_in": '[{"name": "Savor One", "issuer": "Capital One", "score_needed": "Excellent", "description_used" : 1, "card_attributes": "a cool one"}]',
        "return_json": True,
        "max_items_to_parse" : 1,
        "save_to_db": False,
    })
    response = client.post("/parse", content=request_data)
    assert response.status_code == 200
    json_response = response.json()["raw_json_out"][0]
    assert "name" in json_response
    assert "issuer" in json_response
    
def test_extract_with_raw_html():
    request_data = ExtractRequest(
        raw_html = TEST_HTML,
        return_json = True,
        max_items_to_extract = 1,
        save_to_db = False
    )    
    response = client.post("/extract", content=request_data.model_dump_json())
    json_response = response.json()["raw_json_out"]
    assert "name" in json_response
    assert "issuer" in json_response
    assert "score_needed" in json_response
        
    
TEST_HTML = """
<!DOCTYPE html>
<html lang="en-US" style="scroll-behavior: auto;">
<div class="CardDetails mx-0 my-2 py-2 row CardDetails_0" id="CardDetails_A_0">
<div class="col-12"><h2 class="fw-bold mb-3"><a class="sh-active-client sh-quidget-rendered" href="https://www.nextinsure.com/ListingDisplay/display/?passthru=1&amp;src=188961&amp;ccid=4048214&amp;alturl=https%3a%2f%2fwww.cardratings.com%2fbestcards%2ffeatured-credit-cards%3fsrc%3d188961%26shnq%3d4048214%26var1%3dquidget_nomatch&amp;qpl=c5f031e522dbb67a34556bd66ba9fa2c&amp;qrId=67d8774d-b54e-46d5-9070-91dc2d63f605&amp;qrItemId=9101ec72-a7ed-42d1-816f-9c270c3615fa&amp;qdg=1&amp;qurId=6ec83268-b34f-463f-bc01-e53e81097006" data-content="{*api*:*cc*,*credit_card_id*:*4048214*,*field*:*Direct2Client*,*linkTarget*:*_blank*,*linkText*:*card_name*,*linkRel*:*nofollow*}" data-rate-name="Aer Lingus Visa Signature® Card" id="sh-quidget-0" rel="nofollow" target="_blank">Aer Lingus Visa Signature® Card</a></h2></div>
<div class="leftDetail col-sm-3 col-6 order-sm-1 text-center">
<a class="card_art sh-active-client sh-quidget-rendered" href="https://www.nextinsure.com/ListingDisplay/display/?passthru=1&amp;src=188961&amp;ccid=4048214&amp;alturl=https%3a%2f%2fwww.cardratings.com%2fbestcards%2ffeatured-credit-cards%3fsrc%3d188961%26shnq%3d4048214%26var1%3dquidget_nomatch&amp;qpl=c5f031e522dbb67a34556bd66ba9fa2c&amp;qrId=67d8774d-b54e-46d5-9070-91dc2d63f605&amp;qrItemId=9101ec72-a7ed-42d1-816f-9c270c3615fa&amp;qdg=1&amp;qurId=6ec83268-b34f-463f-bc01-e53e81097006" data-content="{*api*:*cc*,*credit_card_id*:*4048214*,*field*:*Direct2ClientLogo*}" data-rate-name="Aer Lingus Visa Signature® Card" id="sh-quidget-1"><img width="130" height="100%" alt="Aer Lingus Visa Signature&amp;#174; Card" target="_blank" rel="sponsored" src="cardratings_files/opt_025.png"></a><div class=" text-center mt-2">
<div class="carditemStar mx-auto ratingStar0"></div>
<span class="about_ratings_info" aria-label="About Our Ratings" title="About Our Ratings" data-bs-toggle="modal" data-bs-target="#aboutOurRatings">About Our Ratings</span>
</div>
<div class="clearBoth"><a class="review_link" target="_blank" href="https://www.cardratings.com/credit-card/aer-lingus-visa-signature-card.html" aria-label="Read our full review" title="Read our full review">Read our full review</a></div>
</div>
<div class="midDetail col-sm-6 order-2 order-sm-2"><span class="sh-active-client sh-quidget-rendered" data-content="{*api*:*cc*,*credit_card_id*:*4048214*,*field*:*description*}" data-rate-name="Aer Lingus Visa Signature® Card" id="sh-quidget-2"><ul><li>Earn 75,000 Avios after you spend $5,000 on purchases within the first three months of account opening.</li><li>Earn 3 Avios per $1 spent on purchases with Aer Lingus, British Airways, Iberia, and LEVEL.</li><li>Earn 2 Avios per $1 spent on hotel accommodations when purchased directly with the hotel.</li><li style="display: list-item;">Every
 calendar year you make purchases of $30,000 on your Aer Lingus Visa 
Signature Card, you'll receive a Commercial Companion Ticket good for 12
 months</li><li style="display: list-item;">You and any authorized users
 on your account are eligible for Priority Boarding on Aer Lingus 
flights departing from and returning to the US from Ireland, subject to 
availability.</li><li style="display: list-item;">Pay no foreign transaction fees when you travel abroad.</li><li style="display: list-item;">Simply
 tap to pay with your contactless Aer Lingus Visa Signature Card. Just 
look for the contactless symbol at checkout. It's fast, easy and secure!</li><li style="display: list-item;">Member FDIC</li></ul><a href="#" onclick="t=(this.innerHTML=='See More');l=document.querySelectorAll('#sh-quidget-2 li');for(x=3;x<l.length;x++){l[x].style.display=(t)?'list-item':'none';}this.innerHTML=(t)?'See Less':'See More';return false;">See Less</a></span></div>
<div class="rightDetail col-sm-3 col-6 order-sm-2">
<div class="buttonDiv"><a class="auto-apply-btn h-auto css-btn apply-btn applyIcon white_color text-center text-decoration-none fst-normal font_16 fw-bold py-2 ps-5 border-0 w-100 sh-active-client sh-quidget-rendered" href="https://www.nextinsure.com/ListingDisplay/display/?passthru=1&amp;src=188961&amp;ccid=4048214&amp;alturl=https%3a%2f%2fwww.cardratings.com%2fbestcards%2ffeatured-credit-cards%3fsrc%3d188961%26shnq%3d4048214%26var1%3dquidget_nomatch&amp;qpl=c5f031e522dbb67a34556bd66ba9fa2c&amp;qrId=67d8774d-b54e-46d5-9070-91dc2d63f605&amp;qrItemId=9101ec72-a7ed-42d1-816f-9c270c3615fa&amp;qdg=1&amp;qurId=6ec83268-b34f-463f-bc01-e53e81097006" data-content="{*api*:*cc*,*credit_card_id*:*4048214*,*field*:*Direct2Client*,*linkTarget*:*_blank*,*linkText*:*APPLY NOW*,*linkRel*:*nofollow*}" data-rate-name="Aer Lingus Visa Signature® Card" id="sh-quidget-3" rel="nofollow" target="_blank">APPLY NOW</a></div>
<div class="credit_div text-center">
<div class="apply_now_bank_name mt-3">on Chase's <br>secure website</div>
<div class="credit_txt mt-3 mb-1">
<span>Credit Needed</span><br><span class="credit_needed font-weight-semibold"><span class="sh-active-client sh-quidget-rendered" data-content="{*api*:*cc*,*credit_card_id*:*4048214*,*field*:*credit_score_needed*}" data-rate-name="Aer Lingus Visa Signature® Card" id="sh-quidget-4">Good/Excellent</span></span>
</div>
</div>
</div>
</div>
</html>
"""

