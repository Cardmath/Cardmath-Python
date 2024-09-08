from creditcard import CreditCard
from scrape import get_card_dict

cc_dict = get_card_dict('cardratings/cardratings.html', 'cardratings/output.txt')

credit_cards = CreditCard.init_from_cc_dict(credit_card_dict=cc_dict, max_num=2, random_samples=True)
for credit_card in credit_cards:
    print(credit_card)
    print("---" * 10)