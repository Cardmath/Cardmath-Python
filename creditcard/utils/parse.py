from creditcard.enums import *
from creditcard.utils.openai import prompt_openai_for_json, benefits_prompt, purchase_category_map_prompt, structure_with_openai, reward_category_map_response_format, benefits_response_format
from pydantic import BaseModel, ConfigDict
from typing import List

RIGHTS_RESERVED = '\u00AE'

class RewardCategoryRelation(BaseModel):
    category : PurchaseCategory
    reward_unit : RewardUnit
    amount : float

    model_config = ConfigDict(from_attributes=True)

# THIS SHOULD ONLY BE CALLED FOR STRUCTURING
class RewardCategoryMap(BaseModel):
    reward_category_map : List[RewardCategoryRelation]

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
    
async def get_reward_category_map(card_description : str) -> List[RewardCategoryRelation]:
    prompt = purchase_category_map_prompt(card_description)
    reward_category_map : RewardCategoryMap= await structure_with_openai(prompt=prompt, response_format=reward_category_map_response_format(), schema=RewardCategoryMap)
    return reward_category_map.reward_category_map

def get_apr(card_description):
    return 0; 