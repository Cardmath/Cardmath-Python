from enums import *
from openai_utils import prompt_gpt4_for_json, benefits_prompt, purchase_category_map_prompt
import json

RIGHTS_RESERVED = '\u00AE'

def get_issuer(card_name): 
    best_issuer = single_nearest(card_name, Issuer)
    if (isinstance(best_issuer, str)): 
        return best_issuer.replace(RIGHTS_RESERVED, "")
    return best_issuer

def get_credit_needed(credit_needed_html_text): 
    return multiple_nearest(credit_needed_html_text, CreditNeeded)
    
def get_benefits(card_attr_list):
    card_attr_list_joined = " - ".join(card_attr_list)
    openai_response = prompt_gpt4_for_json(benefits_prompt(card_attr_list_joined))
    return multiple_nearest(openai_response, Benefit) 
    

def get_reward_category_map(card_attr_list):
    out_rewards = []
    card_attr_list_joined = " - ".join(card_attr_list)
    
    syntactic_openai_response = False
    attempt = 0
    while not syntactic_openai_response:
        attempt += 1
        openai_response = prompt_gpt4_for_json(purchase_category_map_prompt(card_attr_list_joined))    
        try:
            reward_category_map = json.loads(openai_response)
        except ValueError:
            continue
        syntactic_openai_response = True
        print(f"OpenAI succeeded with attempt {attempt}")
        
    for category, reward in reward_category_map.items():
        if isinstance(reward, (tuple, list)) and len(reward) == 2:
            reward_type, reward_amt = reward
        elif isinstance(reward, dict):
            reward_type, reward_amt = list(reward.items())[0]
        else :
            reward_type = None
            reward_amt = 0
            print(f"Unexpected reward format: {category, reward} ")

        
        reward_type = single_nearest(reward_type, RewardUnit)
        try :
            reward_amt = float(reward_amt)
        except ValueError and TypeError:
            reward_amt = 0
            print(f"Unexpected reward amount: {category, reward_amt} ")
        
        out_rewards.append((single_nearest(category, PurchaseCategory), (reward_type, reward_amt)))
    
    return out_rewards

def get_apr(card_attr_list):
    return 0; 