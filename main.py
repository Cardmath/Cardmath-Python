from creditcard import CreditCard
from scrape import get_card_dict

cc_dict = get_card_dict('cardratings/cardratings.html', 'cardratings/output.txt')
credit_cards = CreditCard.init_from_cc_dict(credit_card_dict=cc_dict, max_num=5)

for cc in credit_cards:
    print(cc)