from enums import * 
from scrape import *
from transformers import BertTokenizer, BertModel
import torch


tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
 
def get_issuer(card_dict_key): 
    return 0
    
def get_benefits(card_dict_elem):
    return 0
    
def get_credit_needed(card_dict_elem): 
    return 0

def get_reward_category_map(card_dict_elem): 
    return 0

def encode_text(text):
    # Tokenize the input text and get the input IDs and attention mask
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    
    # Get the embeddings from the BERT model
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_mask)
    
    # Use the embeddings of the [CLS] token (first token) as the sentence embedding
    embeddings = outputs.last_hidden_state[:, 0, :]
    return embeddings

class CreditCard:
    def __init__(self, name, issuer, reward_category_map, benefits, credit_needed):
        self.name = name # Name of Credit Card
        self.issuer = issuer # Name of Issuer
        self.reward_category_map = reward_category_map # Map of Purchase Category -> Reward Units
        self.benefits = benefits  # List of additional Benefits
        self.credit_needed = credit_needed  # CreditNeeded Enum attribute

    def __str__(self):
        return (f"CreditCard(name={self.name}, issuer={self.issuer}, "
                f"rewards={[reward.value for reward in self.rewards]}, "
                f"benefits={[benefit.value for benefit in self.benefits]}, "
                f"credit_needed={self.credit_needed.value})")
        
    def init_from_cc_dict(credit_card_dict): 
        for card_name, card_attributes in credit_card_dict.items():
            issuer = get_issuer(card_name)
            benefits = get_benefits(card_attributes)
            credit_needed = get_credit_needed(card_attributes)
            reward_category_map = get_reward_category_map(card_attributes)
            return CreditCard(card_name, issuer, reward_category_map, benefits, credit_needed)
    
