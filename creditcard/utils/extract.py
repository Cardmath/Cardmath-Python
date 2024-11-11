import logging
from bs4 import BeautifulSoup
from creditcard.schemas import CardRatingsScrapeSchema
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LONG_DESCRIPTION_USED = 0
MEDIUM_DESCRIPTION_USED = 1

def extract_cardratings(raw_html, max_items_to_extract=100) -> List[CardRatingsScrapeSchema]:  
    logger.info("Starting extraction of card ratings.")
    out_card_list = []
    soup = BeautifulSoup(raw_html, 'html.parser')
    cards = soup.find_all(class_="CardDetails")
    logger.info(f"Found {len(cards)} cards to process.")
    
    for i, card in enumerate(cards):
        if len(out_card_list) >= max_items_to_extract:
            logger.info(f"Reached max_items_to_extract limit: {max_items_to_extract}. Stopping extraction.")
            break
        
        logger.info(f"Processing card {i+1}...")
        
        # Initialize variables
        description_used = 1
        issuer = "Issuer not available"
        credit_needed = "Credit score not specified"
        card_title = "Card name not available"
        processed_card_attributes = "Attributes not available"
        
        # Extract card title
        try:
            card_title_tag = card.find('h2').find('a')
            card_title = card_title_tag.get_text(strip=True) if card_title_tag else card_title
            logger.info(f"Card title: {card_title}")
        except Exception as e:
            logger.error(f"Error parsing card title for card {i+1} - {e}")

        # Extract issuer and credit needed information
        try:
            credit_div = card.find(class_='rightDetail').find(class_='credit_div')
            issuer_tag = credit_div.find(class_='apply_now_bank_name')
            credit_needed_tag = credit_div.find(class_='credit_needed')
            issuer = issuer_tag.get_text(strip=True) if issuer_tag else issuer
            credit_needed = credit_needed_tag.get_text(strip=True) if credit_needed_tag else credit_needed
            logger.info(f"Issuer: {issuer}, Credit needed: {credit_needed}")
        except Exception as e:
            logger.error(f"Error parsing issuer and credit needed for card {i+1} - {e}")

        # Extract card attributes (benefits and features)
        try:
            mid_detail = card.find(class_="midDetail")
            if mid_detail and mid_detail.find('ul'):
                card_attributes = mid_detail.find('ul').find_all('li')
                description_used = LONG_DESCRIPTION_USED if mid_detail.find(class_="longDescription") else MEDIUM_DESCRIPTION_USED
                logger.info(f"Description type: {'Long' if description_used == LONG_DESCRIPTION_USED else 'Medium'}")
            else:
                card_attributes = []
                logger.warning(f"No attributes found for card {card_title}. Using default description type.")

            # Process attributes into a formatted string
            if card_attributes:
                processed_card_attributes = "\n - ".join(
                    [attr.get_text(strip=True).replace("\n", "") for attr in card_attributes]
                )
            else:
                logger.warning(f"No card attributes found for {card_title}.")
        except Exception as e:
            logger.error(f"Error parsing card attributes for {card_title} - {e}")

        # Assemble the schema object
        try:
            card_data = CardRatingsScrapeSchema(
                name=card_title,
                description_used=description_used,
                unparsed_issuer=issuer,
                unparsed_credit_needed=credit_needed,
                unparsed_card_attributes=processed_card_attributes
            )
            out_card_list.append(card_data)
            logger.info(f"Card {i+1} processed and added to the list.")
        except Exception as e:
            logger.error(f"Failed to create schema object for card {card_title} - {e}")

    logger.info(f"Extraction completed. Total cards extracted: {len(out_card_list)}.")
    return out_card_list