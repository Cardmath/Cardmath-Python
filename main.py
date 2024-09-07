from creditcard import CreditCard
from scrape import get_card_dict
import random

cc_dict = get_card_dict('cardratings/cardratings.html', 'cardratings/output.txt')

# TODO ALLOW FOR RANDOM SAMPLES
credit_cards = CreditCard.init_from_cc_dict(credit_card_dict=cc_dict, max_num=5, random_samples=True)
for credit_card in credit_cards:
    print(credit_card)
    print("---" * 10)