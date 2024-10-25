from creditcard.enums import *
from creditcard.utils.openai import *
from pydantic import BaseModel, ConfigDict, field_validator, field_serializer
from typing import List, Union
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
    
class RewardCategoryRelation(BaseModel):
    category : PurchaseCategory
    reward_unit : RewardUnit
    amount : float

    model_config = ConfigDict(from_attributes=True)

    @field_validator('amount')
    def amount_must_be_reasonable(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Amount must be positive and less than 100 to be reasonable')
        return v

# THIS SHOULD ONLY BE CALLED FOR STRUCTURING
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

    model_config = ConfigDict(from_attributes=True)

async def get_sign_on_bonus(card_description : str):
    prompt = conditional_sign_on_bonus_prompt(card_description)
    response : ConditionalSignOnBonusResponse = await structure_with_openai(prompt=prompt, response_format=conditional_sign_on_bonus_response_format(), schema=ConditionalSignOnBonusResponse)
    return response.conditional_sign_on_bonus

class APR(BaseModel):
    apr : float
    type : APRType

    model_config = ConfigDict(from_attributes=True)

    @field_validator('apr')
    def apr_must_be_reasonable(cls, v):
        if v < 0 or v > 100:
            raise ValueError('APR must be positive and less than 100 to be reasonable')
        return v 

class APRResponse(BaseModel):
    apr_list : List[APR] 

async def get_apr(card_description):
    prompt = apr_prompt(card_description)
    apr: APRResponse = await structure_with_openai(prompt=prompt, response_format=apr_response_format(), schema=APRResponse)
    return TypeAdapter(List[APR]).dump_python(apr.apr_list)

class AnnualFee(BaseModel):
    fee_usd : float = 0
    waived_for : int = 0

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

    model_config = ConfigDict(from_attributes=True)

class AnnualFeeResponse(BaseModel):
    annual_fee: AnnualFee

    model_config = ConfigDict(from_attributes=True)

async def get_annual_fee(card_description):
    prompt = annual_fee_prompt(card_description)
    annual_fee = await structure_with_openai(prompt, response_format=annual_fee_response_format(), schema=AnnualFeeResponse)
    return annual_fee