from enums import *
from openai_utils import prompt_gpt4_for_json, benefits_prompt, purchase_category_map_prompt
import json

RIGHTS_RESERVED = '\u00AE'

def get_issuer(card_name): 
    best_issuer = None
    for issuer in Issuer:
        if issuer in card_name:
            best_issuer = issuer   
    if best_issuer is None:   
        print(f"No issuer matched for: {card_name}")
        return " Unknown Issuer "
    
    return best_issuer.replace(RIGHTS_RESERVED, "")

def get_credit_needed(credit_needed_html_text): 
    credit_needed_out = []
    for credit_range in CreditNeeded:
        if credit_range in credit_needed_html_text:
            credit_needed_out.append(credit_range)   
    if credit_needed_out is None:   
        print(f"No credit scores matched for: {credit_needed_html_text}")
    
    return credit_needed_out
    
def get_benefits(card_attr_list):
    out_benefits = []
    card_attr_list_joined = " - ".join(card_attr_list)
    
    openai_response = prompt_gpt4_for_json(benefits_prompt(card_attr_list_joined))
    
    for benefit in Benefits:
        if strip_up_to_period(benefit) in openai_response:
            out_benefits.append(benefit)   
    
    if out_benefits is None:   
        print(f"No benefits matched for: {card_attr_list}")
    
    return out_benefits

def get_reward_category_map(card_attr_list):
    out_benefits = []
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
        
        out_benefits = []
        for category, reward in reward_category_map.items():
            out_benefits.append((category, reward))
        
    return out_benefits

def get_apr(card_attr_list):
    return 0; 

def strip_up_to_period(text):
    parts = text.split('.', 1)  # Split the text at the first period
    if len(parts) > 1:
        return parts[1].strip()  # Return the part after the period, stripped of leading/trailing whitespace
    return text.strip()  # If no period is found, return the original text stripped of leading/trailing whitespace
