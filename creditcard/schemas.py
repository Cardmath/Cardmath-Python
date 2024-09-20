from creditcard.utils.parse import *
from database.creditcard.creditcard import CreditCard
from database.scrapes.cardratings import CardratingsScrape
from pydantic import BaseModel, ConfigDict
from typing import List

import json

class CardRatingsScrapeSchema(BaseModel):
    name: str
    description_used: int
    unparsed_issuer: str
    unparsed_credit_needed: str
    unparsed_card_attributes: str
    
    model_config = ConfigDict(from_attributes=True)

    def credit_card_schema(self):
        name = self.name.replace('\u00AE', '')
        issuer = get_issuer(self.unparsed_issuer)
        benefits = get_benefits(self.unparsed_card_attributes)
        credit_needed = get_credit_needed(self.unparsed_credit_needed)
        reward_category_map = get_reward_category_map(self.unparsed_card_attributes)
        apr = get_apr(self.unparsed_card_attributes)
        return CreditCardSchema(name=name, 
                          issuer=issuer,
                          benefits=benefits,
                          credit_needed=credit_needed,
                          reward_category_map=reward_category_map,
                          apr=apr)
        
    def cardratings_scrape(self):
        return CardratingsScrape(
            name = self.name,
            description_used = self.description_used,
            unparsed_issuer=self.unparsed_issuer,
            unparsed_card_attributes=self.unparsed_card_attributes,
            unparsed_credit_needed=self.unparsed_credit_needed
        )
        
class CreditCardSchema(BaseModel):
    name : str 
    issuer : Issuer
    reward_category_map : List[RewardCategoryRelation]
    benefits : List[Benefit]
    credit_needed : List[CreditNeeded]
    apr : float
    
    def reward_category_map_json(self) -> str:
        rewards : List[str] = [reward_category_relation.model_dump_json() for reward_category_relation in self.reward_category_map]
        return json.dumps(rewards)
    
    def benefits_json(self) -> str:
        benefits_list = [benefit.value for benefit in self.benefits]
        return json.dumps(benefits_list)
    
    def credit_needed_json(self) -> str:
        credits : List[str] = [credit.value for credit in self.credit_needed]
        return json.dumps(credits)
    
    def credit_card(self) -> CreditCard:
        return CreditCard(name=self.name, 
                          issuer=self.issuer,
                          benefits=self.benefits_json(),
                          credit_needed=self.credit_needed_json(),
                          reward_category_map=self.reward_category_map_json(),
                          apr=self.apr)
