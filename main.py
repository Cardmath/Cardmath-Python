from creditcard import CreditCard
from scrape import get_card_dict

cc_dict = get_card_dict('cardratings/cardratings.html', 'cardratings/output.txt')
credit_cards = CreditCard.init_from_cc_dict(cc_dict)
print(credit_cards)