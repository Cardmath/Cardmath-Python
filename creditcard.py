from enums import * 
from scrape import *
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertModel, BertTokenizer
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

    for card_attr in card_attr_list:
        for benefit in Benefits: 
            # initialize dictionaries
            if benefit not in encoded_benefits:
                encoded_benefits[benefit] = encode_text(benefit.value)
            if benefit not in benefit_score :
                benefit_score[benefit] = 0
            
            encoded_attr = encode_text(card_attr)
            attr_benefit_score = cosine_similarity(encoded_benefits[benefit], encoded_attr)[0][0]
            benefit_score[benefit] += attr_benefit_score

    out_benefits = []
    for benefit in Benefits:
        if benefit_score[benefit] >= 5:
            out_benefits.append(benefit)
    return out_benefits
    
def get_credit_needed(card_dict_elem): 
    return 0

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

class CreditCard:
    def __init__(self, name, issuer, reward_category_map, benefits, credit_needed):
        self.name = name # Name of Credit Card
        self.issuer = issuer # Name of Issuer
        self.reward_category_map = reward_category_map # Map of Purchase Category -> Reward Units
        self.benefits = benefits  # List of additional Benefits
        self.credit_needed = credit_needed  # CreditNeeded Enum attribute

    def __str__(self):
        return (f"CreditCard(name={self.name}, issuer={self.issuer}, "
                f"rewards={self.reward_category_map}, "
                f"benefits={[benefit.value for benefit in self.benefits]}, "
                f"credit_needed={self.credit_needed})")
        
    def init_from_cc_dict(credit_card_dict): 
        for card_details, card_attributes in credit_card_dict.items():
            cc_issuer, cc_name = card_details
            issuer = get_issuer(cc_issuer)
            benefits = get_benefits(card_attributes)
            credit_needed = get_credit_needed(card_attributes)
            reward_category_map = get_reward_category_map(card_attributes)
            return CreditCard(cc_name, issuer, reward_category_map, benefits, credit_needed)


cc_dict = get_card_dict('/home/johannes/CreditCards/cardratings/cardratings.html', None)
credit_cards = CreditCard.init_from_cc_dict(cc_dict)
print(credit_cards)
        