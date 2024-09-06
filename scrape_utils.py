from enums import *
from openai_utils import prompt_gpt4_for_json, benefits_prompt

def get_issuer(card_name): 
    best_issuer = None
    for issuer in Issuer:
        if issuer in card_name:
            best_issuer = issuer   
    if issuer is None:   
        print(f"No issuer mathced for: {card_name}")
    
    return best_issuer

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

def get_reward_category_map(card_dict_elem): 
    return 0

def strip_up_to_period(text):
    parts = text.split('.', 1)  # Split the text at the first period
    if len(parts) > 1:
        return parts[1].strip()  # Return the part after the period, stripped of leading/trailing whitespace
    return text.strip()  # If no period is found, return the original text stripped of leading/trailing whitespace
