from enums import *
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
 
def get_issuer(card_name): 
    best_issuer = None
    for issuer in Issuer:
        if issuer in card_name:
            best_issuer = issuer   
    if issuer is None:   
        print(f"No issuer mathced for: {card_name}")
    
    return best_issuer
    
def get_benefits(card_attr_list):
    benefit_score = {} # dict of Benefit enum item and score (real number)
    encoded_benefits = {} # dict of the Benefit to their encoded value 
    out_benefits = []
    
    for card_attr in card_attr_list:
        for benefit in Benefits: 
            # initialize dictionaries
            if benefit not in encoded_benefits:
                encoded_benefits[benefit] = encode_text(benefit.value)
            if benefit not in benefit_score :
                benefit_score[benefit] = 0
            
            encoded_attr = encode_text(card_attr)
            attr_benefit_score = cosine_similarity(encoded_benefits[benefit], encoded_attr)[0][0]
            if (attr_benefit_score) > 0.85:
                out_benefits.append(benefit)
    
    return out_benefits
                

    
def get_credit_needed(credit_needed): 
    best_credit_out = []
    for credit in CreditNeeded:
        if credit in credit_needed:
            best_credit_out.append(credit)   
    if best_credit_out is None:   
        print(f"No credit scores matched for: {credit_needed}")
    
    return best_credit_out

def get_reward_category_map(card_dict_elem): 
    return 0

def encode_text(text):
    # Tokenize the input text and get the input IDs and attention mask
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    
    # Get the embeddings from the Bert model
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    
    # Use the embeddings of the [CLS] token (first token) as the sentence embedding
    embeddings = outputs.last_hidden_state[:, 0, :]
    return embeddings
