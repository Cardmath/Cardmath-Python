from creditcard.enums import *
from creditcard.utils.openai import *
from pydantic import BaseModel, ConfigDict, field_validator, field_serializer
from typing import List, Union, Optional
from datetime import timedelta

RIGHTS_RESERVED = '\u00AE'

def get_issuer(card_name : str): 
    best_issuer = single_nearest(card_name, Issuer)
    if (isinstance(best_issuer, str)): 
        return best_issuer.replace(RIGHTS_RESERVED, "")
    return best_issuer

def get_credit_needed(credit_needed_html_text : str): 
    return multiple_nearest(credit_needed_html_text, CreditNeeded)
    
async def get_benefits(card_description : str):
    openai_response = await prompt_openai_for_json(benefits_prompt(card_description), response_format=benefits_response_format())
    return multiple_nearest(openai_response, Benefit) 

class RewardCategoryThreshold(BaseModel):
    on_up_to_purchase_amount_usd: float
    per_timeframe_num_months: int
    fallback_reward_amount: float

    model_config = ConfigDict(from_attributes=True)

    @field_validator('fallback_reward_amount', mode="before")
    @classmethod
    def amount_must_be_reasonable(cls, v):
        if v < 0 or v > 10:
            raise ValueError('Amount must be positive and less than 20 to be reasonable')
        return v

class RewardCategoryRelation(BaseModel):
    category : Union[PurchaseCategory, Vendors]
    reward_unit : RewardUnit
    reward_amount : float

    reward_threshold : Optional[RewardCategoryThreshold] = None
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator('reward_amount', mode="before")
    @classmethod
    def amount_must_be_reasonable(cls, v):
        if v < 0 or v > 20:
            raise ValueError('Amount must be positive and less than 20 to be reasonable')
        return v
    
    @field_validator('reward_threshold', mode="before")
    @classmethod
    def validate_threshold(cls, v):
        if v is not None:
            v = RewardCategoryThreshold.model_validate(v)
            if v.on_up_to_purchase_amount_usd < 0 or v.per_timeframe_num_months < 0:
                return None
            else :
                return v

class RewardCategoryMap(BaseModel):
    reward_category_map : List[RewardCategoryRelation]

async def get_reward_category_map(card_description : str) -> List[RewardCategoryRelation]:
    prompt = purchase_category_map_prompt(card_description)
    reward_category_map : RewardCategoryMap= await structure_with_openai(prompt=prompt, response_format=reward_category_map_response_format(), schema=RewardCategoryMap)
    return reward_category_map.reward_category_map

class ConditionalSignOnBonus(BaseModel):
    purchase_type: Union[PurchaseCategory, Vendors]
    condition_amount: float
    timeframe: timedelta

    reward_type: RewardUnit
    reward_amount: float

    model_config = ConfigDict(from_attributes=True)

    @field_validator('timeframe', mode="before")
    @classmethod
    def parse_as_months(cls, v):
        if isinstance(v, (int, float)):
            return timedelta(days=30 * v)
        return v

    @field_serializer('timeframe')
    @classmethod
    def serialize_as_months(cls, v):
        if isinstance(v, timedelta):
            return v.days / 30
        
    def get_timeframe_in_months(self):
        return self.timeframe.days / 30

class ConditionalSignOnBonusResponse(BaseModel):
    conditional_sign_on_bonus : List[ConditionalSignOnBonus]

async def get_sign_on_bonus(card_description : str):
    prompt = conditional_sign_on_bonus_prompt(card_description)
    response : ConditionalSignOnBonusResponse = await structure_with_openai(prompt=prompt, response_format=conditional_sign_on_bonus_response_format(), schema=ConditionalSignOnBonusResponse)
    return response.conditional_sign_on_bonus

class APR(BaseModel):
    apr : float
    apr_type : APRType
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator('apr', mode="before")
    def apr_must_be_reasonable(cls, v):
        if v < 0 or v > 100:
            raise ValueError('APR must be positive and less than 100 to be reasonable')
        return v 

class APRResponse(BaseModel):
    apr_list : List[APR] 

async def get_apr(card_description):
    prompt = apr_prompt(card_description)
    apr: APRResponse = await structure_with_openai(prompt=prompt, response_format=apr_response_format(), schema=APRResponse)
    return apr.apr_list

class AnnualFee(BaseModel):
    fee_usd : float
    waived_for : int

    model_config = ConfigDict(from_attributes=True)

    @field_validator('fee_usd')
    def fee_usd_must_be_reasonable(cls, v):
        if v < 0:
            raise ValueError('Fee must be positive to be reasonable')
        return v
    
    @field_validator('waived_for')
    def waived_for_must_be_reasonable(cls, v):
        if v < 0:
            raise ValueError('Waived for must be positive to be reasonable')
        return v

class AnnualFeeResponse(BaseModel):
    annual_fee: AnnualFee

async def get_annual_fee(card_description):
    prompt = annual_fee_prompt(card_description)
    annual_fee: AnnualFeeResponse = await structure_with_openai(prompt, response_format=annual_fee_response_format(), schema=AnnualFeeResponse)
    return annual_fee.annual_fee

class CreditCardKeywordResponse(BaseModel):
    card_keywords: List[CreditCardKeyword]

async def get_keywords(card_description, card_tile : str = ""):
    prompt = card_keywords_prompt("Card: " + card_tile + "\n" + card_description)
    keywords: CreditCardKeywordResponse = await structure_with_openai(prompt, response_format=card_keywords_response_format(), schema=CreditCardKeywordResponse)
    return keywords.card_keywords

class PeriodicStatementCredit(BaseModel): 
    credit_amount: float # in dollars
    unit: RewardUnit 
    categories: List[PurchaseCategory] # purchase categories where the statement credit can be used
    vendors: List[Vendors] # stores where the statement credit can be used
    timeframe_months: int
    max_uses: int

    description: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator('timeframe_months', mode="before")
    def timeframe_must_be_reasonable(cls, v):
        if v < 0:
            raise ValueError('Timeframe must be positive to be reasonable')
        return v

class PeriodicStatementCreditResponse(BaseModel):
    periodic_statement_credit: List[PeriodicStatementCredit]

async def get_statement_credit(card_description, card_tile : str = ""):
    prompt = statement_credit_prompt("Card: " + card_tile + "\n" + card_description)
    periodic_statement_credit_response: PeriodicStatementCreditResponse = await structure_with_openai(prompt, response_format=periodic_statement_credit_response_format(), schema=PeriodicStatementCreditResponse)
    return periodic_statement_credit_response.periodic_statement_credit