from collections import defaultdict
from creditcard.enums import *  
from creditcard.utils.parse import *
from database.creditcard.creditcard import CreditCard
from database.scrapes.cardratings import CardratingsScrape
from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator, TypeAdapter
from typing import List
from typing import Optional, Union

import json

def get_primary_reward_unit(reward_category_map: List[RewardCategoryRelation]) -> RewardUnit:
    if not reward_category_map:
        return RewardUnit.UNKNOWN

    # Dictionary to count occurrences of each RewardUnit
    reward_unit_counts = defaultdict(int)
    
    # Count each reward unit occurrence
    for relation in reward_category_map:
        reward_unit_counts[relation.reward_unit] += 1

    # Find the RewardUnit with the maximum count
    primary_reward_unit = max(reward_unit_counts, key=reward_unit_counts.get)
    return primary_reward_unit

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
        primary_reward_unit = get_primary_reward_unit(reward_category_map)
        apr = await get_apr(self.unparsed_card_attributes)
        sign_on_bonus = await get_sign_on_bonus(self.unparsed_card_attributes)
        annual_fee = await get_annual_fee(self.unparsed_card_attributes)
        statement_credit = await get_statement_credit(self.unparsed_card_attributes, card_tile=name)
        keywords = await get_keywords(self.unparsed_card_attributes, name)

        return CreditCardSchema(name=name, 
                          issuer=issuer,
                          benefits=benefits,
                          credit_needed=credit_needed,
                          reward_category_map=reward_category_map,
                          sign_on_bonus=sign_on_bonus,
                          apr=apr,
                          annual_fee=annual_fee,
                          statement_credit=statement_credit,
                          primary_reward_unit=primary_reward_unit,
                          keywords=keywords)
        
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
    annual_fee: Optional[AnnualFee] = None
    statement_credit: List[PeriodicStatementCredit]
    primary_reward_unit: RewardUnit
    keywords: List[CreditCardKeyword]

    model_config = ConfigDict(from_attributes=True)

    @field_validator('sign_on_bonus', mode='before')
    @classmethod
    def validate_sign_on_bonus(cls, v):
        if isinstance(v, list):
            return [ConditionalSignOnBonus.model_validate(sign_on_bonus) for sign_on_bonus in v]

        return v


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
                          apr=TypeAdapter(List[APR]).dump_python(self.apr),
                          annual_fee = self.annual_fee.model_dump(),
                          keywords= TypeAdapter(List[CreditCardKeyword]).dump_python(self.keywords),
                          statement_credit=TypeAdapter(List[PeriodicStatementCredit]).dump_python(self.statement_credit),
                          primary_reward_unit=self.primary_reward_unit)
    
class CreditCardRecommendationSchema(CreditCardSchema):
    status: CardAction

    @classmethod
    def from_credit_card_schema(cls, schema: CreditCardSchema, status: CardAction):
        return cls(
            name=schema.name,
            issuer=schema.issuer,
            reward_category_map=schema.reward_category_map,
            benefits=schema.benefits,
            credit_needed=schema.credit_needed,
            apr=schema.apr,
            sign_on_bonus=schema.sign_on_bonus,
            annual_fee=schema.annual_fee,
            statement_credit=schema.statement_credit,
            primary_reward_unit=schema.primary_reward_unit,
            keywords=schema.keywords,
            status=status
        )

class CreditCardsFilter(BaseModel):
    id_in_db : Optional[List[int]]
    issuer : Optional[List[Issuer]]
    credit_needed : Optional[List[CreditNeeded]]
    benefits : Optional[List[Benefit]]
    apr : Optional[float]

class CreditCardsDatabaseRequest(BaseModel):
    card_details: Union[str, CreditCardsFilter] = "all"
    use_preferences: bool
    max_num : Optional[int] = None

    @field_validator('card_details')
    @classmethod
    def validate_card_details(cls, v):
        if isinstance(v, str) and v != "all":
            raise ValueError('must be all or a filter')
        
        return v

class CreditCardsDatabaseResponse(BaseModel):
    credit_card: List[CreditCardSchema]

class CardInWalletSchema(BaseModel):
    is_held : bool
    credit_card_id: int
    wallet_id: Optional[int]
    card : CreditCardSchema

    model_config = ConfigDict(from_attributes=True)

class WalletSchema(BaseModel):
    id : int
    name : str
    last_edited : date
    is_custom : bool
    cards: List[CardInWalletSchema]

    model_config = ConfigDict(from_attributes=True)


class CardLookupSchema(BaseModel):
    name: str
    issuer: str
    
    model_config = ConfigDict(from_attributes=True)

class WalletsIngestRequest(BaseModel):
    name : str
    cards : List[CardLookupSchema]
    is_custom : bool

    model_config = ConfigDict(from_attributes=True)

class WalletDeleteRequest(BaseModel):
    wallet_id: int

class WalletUpdateRequest(BaseModel):
    wallet_id: int
    name: Optional[str]
    is_custom: Optional[bool]
    cards: Optional[List[CardLookupSchema]]