from bs4 import BeautifulSoup
from creditcard.schemas import CreditCardCreate

cardratings_scraped_path = '/home/johannes/CreditCards/cardratings/cardratings.html'

LONG_DESCRIPTION_USED = 0
MEDIUM_DESCRIPTION_USED = 1


# Produces a dictionary of form:
# (issuer, card name) --> [card attr_0, card_attr_1, ...] 
# where card attr is a plain text string
def extract_cardratings(raw_html, max_items_to_extract=100):  
    out_card_list = []
    soup = BeautifulSoup(raw_html, 'html.parser')
    cards = soup.find_all(class_="CardDetails")
    
    for card in cards:
        if (len(out_card_list) >= max_items_to_extract):
            return out_card_list
        
        description_used = None
        credit_div = card.find(class_='rightDetail').find(class_='credit_div')
        issuer = credit_div.find(class_='apply_now_bank_name')
        credit_needed = credit_div.find(class_='credit_needed')
        card_title = card.find('h2')
        mid_detail = card.find(class_="midDetail")
        
        if mid_detail.find(class_="longDescription"):
            card_attributes = mid_detail.find(class_="longDescription").find('ul').findAll('li')
            description_used = LONG_DESCRIPTION_USED    
        else:
            card_attributes = card.find('ul')
            if card_attributes is not None:
                card_attributes = card_attributes.findAll('li')
            description_used = MEDIUM_DESCRIPTION_USED
        
        processed_card_attributes : str = "" 
        if card_attributes is not None and isinstance(card_attributes, list):
            processed_card_attributes = "\n - ".join([card_attribute.get_text(strip=True).replace("\n", "") for card_attribute in card_attributes])
            
        card = CreditCardCreate(name= card_title.get_text(strip=True),
                issuer= issuer.get_text(strip=True),
                score_needed= credit_needed.get_text(strip=True),
                description_used= description_used,
                card_attributes= processed_card_attributes).model_dump_json()
        
        out_card_list.append(card)
        
    return out_card_list