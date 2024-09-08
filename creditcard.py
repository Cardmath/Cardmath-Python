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
    credit_needed: List[CreditNeeded]
    apr: float
    
    def __str__(self):
        return (f"CreditCard(name={self.name}, issuer={self.issuer}, "
                f"rewards={self.reward_category_map}, "
                f"benefits={[benefit.value for benefit in self.benefits]}, "
                f"credit_needed={self.credit_needed})")
    
    @staticmethod
    def init_from_str_tuple(credit_card_tuple : tuple):        
        if len(credit_card_tuple) == 2:
            (name, issuer, score_needed, description_used), card_attributes = credit_card_tuple
        elif len(credit_card_tuple) == 1:
            id, name, issuer, score_needed, description_used, card_attributes = credit_card_tuple[0]
        else :
            print("Invalid tuple length.")
            return None
        
        name = name.replace('\u00AE', '')
        issuer = get_issuer(issuer)
        benefits = get_benefits(card_attributes)
        credit_needed = get_credit_needed(score_needed)
        reward_category_map = get_reward_category_map(card_attributes)
        apr = get_apr(card_attributes)
        return CreditCard(name, issuer, reward_category_map, benefits, credit_needed, apr)
        
    @staticmethod
    def init_from_cc_dict(credit_card_dict : dict, max_num : int, random_samples : bool = False): 
        if random_samples:
            credit_card_dict = random.sample(list(credit_card_dict.items()), max_num)
        
        credit_cards = []
        for idx, credit_card_tuple in enumerate(credit_card_dict):
            if idx == max_num:
                return credit_cards    
            parsed_card = CreditCard.init_from_str_tuple(credit_card_tuple)
            credit_cards.append(parsed_card)
        
        return credit_cards
    

        