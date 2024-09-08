from enums import * 
from scrape_utils import *
import random
from dataclasses import dataclass
from typing import List, Dict

@dataclass(frozen=True)
class CreditCard:
    name: str
    issuer: Issuer
    reward_category_map: List[Dict[PurchaseCategory, float]]
    benefits: List[Benefit]
    credit_needed: list[CreditNeeded]
    apr: float
    
    def __str__(self):
        return (f"CreditCard(name={self.name}, issuer={self.issuer}, "
                f"rewards={self.reward_category_map}, "
                f"benefits={[benefit.value for benefit in self.benefits]}, "
                f"credit_needed={self.credit_needed})")
    
    @staticmethod
    def init_from_cc_dict(credit_card_dict, max_num, random_samples=False): 
        credit_cards = []
        if random_samples:
            credit_card_dict = random.sample(list(credit_card_dict.items()), max_num)
        
        for idx, val in enumerate(credit_card_dict):
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
        