from bs4 import BeautifulSoup
from creditcard.schemas import CardRatingsScrapeSchema
from typing import List

LONG_DESCRIPTION_USED = 0
MEDIUM_DESCRIPTION_USED = 1

def extract_cardratings(raw_html, max_items_to_extract=100) -> List[CardRatingsScrapeSchema]:  
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
        elif card_attributes is not None:
            processed_card_attributes = card_attributes.get_text(strip=True)
        else :
            raise ValueError(f"Found no card attributes for {card_title.get_text(strip=True)}")
            
        if processed_card_attributes == "":
            print(f"Found no card attributes for {card_title.get_text(strip=True)}")

        if issuer.get_text(strip=True) is None:
            print(f"Found no issuer for {card_title.get_text(strip=True)}")

        card = CardRatingsScrapeSchema(name = card_title.get_text(strip=True),
                description_used= description_used,
                unparsed_issuer = issuer.get_text(strip=True),
                unparsed_credit_needed = credit_needed.get_text(strip=True),
                unparsed_card_attributes = processed_card_attributes)
        
        out_card_list.append(card)
        
    return out_card_list