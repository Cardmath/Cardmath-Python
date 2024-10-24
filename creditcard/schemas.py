from creditcard.enums import *  
from creditcard.utils.parse import *
from database.creditcard.creditcard import CreditCard
from database.scrapes.cardratings import CardratingsScrape
from pydantic import BaseModel, ConfigDict, field_validator, TypeAdapter
from typing import List
from typing import Optional, Union

import json

class CardRatingsScrapeSchema(BaseModel):
    name: str
    description_used: int
    unparsed_issuer: str
    unparsed_credit_needed: str
    unparsed_card_attributes: str
    
    model_config = ConfigDict(from_attributes=True)

    async def credit_card_schema(self):
        name = self.name.replace('\u00AE', '')
        issuer = get_issuer(self.unparsed_issuer)
        benefits = await get_benefits(self.unparsed_card_attributes)
        credit_needed = get_credit_needed(self.unparsed_credit_needed)
        reward_category_map = await get_reward_category_map(self.unparsed_card_attributes)
        apr = await get_apr(self.unparsed_card_attributes)
        sign_on_bonus = await get_sign_on_bonus(self.unparsed_card_attributes)
        return CreditCardSchema(name=name, 
                          issuer=issuer,
                          benefits=benefits,
                          credit_needed=credit_needed,
                          reward_category_map=reward_category_map,
                          sign_on_bonus=sign_on_bonus,
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
    apr : List[APR]
    sign_on_bonus : Optional[List[ConditionalSignOnBonus]] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('reward_category_map', mode='before')
    @classmethod
    def validate_reward_category_map(cls, v):
        if isinstance(v, str):
            v = json.loads(v)
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], str): 
                v = [RewardCategoryRelation.model_validate_json(rc_relation) for rc_relation in v]  

        return v 
    
    @field_validator('benefits', mode='before')
    @classmethod
    def validate_benefits(cls, v):
        if isinstance(v, str):
            v = json.loads(v)
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], str):
                v = [single_nearest(benefit, Benefit) for benefit in v]
        
        if not isinstance(v, list):
            raise ValueError("Input should be a valid list")

        return v 
    
    @field_validator('credit_needed', mode='before')
    @classmethod
    def validate_credit_needed(cls, v):
        if isinstance(v, str):
            v = json.loads(v)
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], str):
                v = [single_nearest(credit_needed, CreditNeeded) for credit_needed in v]
        
        if not isinstance(v, list):
            raise ValueError("Input should be a valid list")

        return v 
    
    def credit_card(self) -> CreditCard:
        return CreditCard(name=self.name, 
                          issuer=self.issuer,
                          benefits=TypeAdapter(List[Benefit]).dump_python(self.benefits),
                          credit_needed=TypeAdapter(List[CreditNeeded]).dump_python(self.credit_needed),
                          reward_category_map=TypeAdapter(List[RewardCategoryRelation]).dump_python(self.reward_category_map),
                          sign_on_bonus=TypeAdapter(List[ConditionalSignOnBonus]).dump_python(self.sign_on_bonus),
                          apr=TypeAdapter(List[APR]).dump_python(self.apr))

class CreditCardsFilter(BaseModel):
    id_in_db : Optional[List[int]]
    issuer : Optional[List[Issuer]]
    credit_needed : Optional[List[CreditNeeded]]
    benefits : Optional[List[Benefit]]
    apr : Optional[float]

class CreditCardsDatabaseRequest(BaseModel):
    card_details: Union[str, CreditCardsFilter] = "all"
    max_num : Optional[int] = None

    @field_validator('card_details')
    @classmethod
    def validate_card_details(cls, v):
        if isinstance(v, str) and v != "all":
            raise ValueError('must be all or a filter')
        
        return v

class CreditCardsDatabaseResponse(BaseModel):
    credit_card: List[CreditCardSchema]