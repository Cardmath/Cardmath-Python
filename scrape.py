from bs4 import BeautifulSoup
from pprint import pformat

cardratings_scraped_path = '/home/johannes/CreditCards/cardratings/cardratings.html'

LONG_DESCRIPTION_USED = 0
MEDIUM_DESCRIPTION_USED = 1


# Produces a dictionary of form:
# (issuer, card name) --> [card attr_0, card_attr_1, ...] 
# where card attr is a plain text string
def get_card_dict(input_file):  
    card_dict = {}
    long_description_used = 0
    mid_description_used = 0

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            response = file.read()
        soup = BeautifulSoup(response, 'html.parser')
        cards = soup.find_all(class_="CardDetails")
        print(f"Found {len(cards)} cards.")
        
        for card in cards:
            description_used = None
            credit_div = card.find(class_='rightDetail').find(class_='credit_div')
            issuer = credit_div.find(class_='apply_now_bank_name')
            credit_needed = credit_div.find(class_='credit_needed')
            card_title = card.find('h2')
            mid_detail = card.find(class_="midDetail")
            
            if mid_detail.find(class_="longDescription"):
                card_attributes = mid_detail.find(class_="longDescription").find('ul').findAll('li')
                long_description_used += 1
                description_used = LONG_DESCRIPTION_USED    
            else:
                card_attributes = card.find('ul').findAll('li')
                mid_description_used += 1
                description_used = MEDIUM_DESCRIPTION_USED
            
            card_dict[(card_title.get_text(strip=True), issuer.get_text(strip=True), credit_needed.get_text(strip=True), description_used)] = "\n - ".join([card_attribute.get_text(strip=True) for card_attribute in card_attributes])
            
        print(f"Long description used: {long_description_used}")
        print(f"Mid description used: {mid_description_used}")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    return card_dict