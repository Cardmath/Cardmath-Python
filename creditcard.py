from enums import * 
from scrape_utils import *

class CreditCard:
    def __init__(self, name, issuer, reward_category_map, benefits, credit_needed, apr):
        self.name = name # Name of Credit Card
        self.issuer = issuer # Name of Issuer
        self.reward_category_map = reward_category_map # Map of Purchase Category -> Reward Units
        self.benefits = benefits  # List of additional Benefits
        self.credit_needed = credit_needed  # CreditNeeded Enum attribute
        self.apr = apr # apr object

    def __str__(self):
        return (f"CreditCard(name={self.name}, issuer={self.issuer}, "
                f"rewards={self.reward_category_map}, "
                f"benefits={[benefit.value for benefit in self.benefits]}, "
                f"credit_needed={self.credit_needed})")
    
    @staticmethod
    def init_from_cc_dict(credit_card_dict, max_num): 
        credit_cards = []
        for idx, val in enumerate(credit_card_dict.items()):
            
            if idx == max_num:
                return credit_cards
            
            print(" --- " + str(idx + 1) + " ---")
            
            card_details, card_attributes = val
            cc_issuer, cc_name, score_needed = card_details
            cc_name = cc_name.replace('\u00AE', '')
            issuer = get_issuer(cc_issuer)
            benefits = get_benefits(card_attributes)
            credit_needed = get_credit_needed(score_needed)
            reward_category_map = get_reward_category_map(card_attributes)
            apr = get_apr(card_attributes)
            
            credit_card = CreditCard(cc_name, issuer, reward_category_map, benefits, credit_needed, apr)
            credit_cards.append(credit_card)
        
        return credit_cards
        