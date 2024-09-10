import pytest
from fastapi.testclient import TestClient
from app import app, parse, ParseRequest, ParseResponse, ExtractRequest
import json

client = TestClient(app)

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
    assert "card_title" in json_response
    assert "issuer" in json_response
    assert "credit_needed" in json_response
    
# TODO WRITE DOWNLOAD TESTS
    
    
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

