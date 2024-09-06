from creditcard import CreditCard
from scrape import get_card_dict

cc_dict = get_card_dict('/home/johannes/CreditCards/cardratings/cardratings.html', None)
credit_cards = CreditCard.init_from_cc_dict(cc_dict)
print(credit_cards)