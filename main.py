from creditcard import CreditCard
from scrape import get_card_dict
from database.sqlite_impl import SQLiteImpl
import pandas as pd

max_num_card = 2
db = SQLiteImpl()
db.connect('creditcards.db')
db.create_unparsed_data_table()
credit_cards = []

if (db.is_empty()):
    cc_dict = get_card_dict('cardratings/cardratings.html')

    for idx, ((name, issuer, score_needed, description_used), card_attributes) in enumerate(cc_dict.items()):
        db.update_unparsed_data_table_entry(idx, name, issuer, score_needed, card_attributes, description_used)

    credit_cards = CreditCard.init_from_cc_dict(credit_card_dict=cc_dict, max_num=max_num_card, random_samples=True)
else :
    for id in range(min(db.count_rows("unparsed_data"), max_num_card)):
            condition = f"id = {id}"
            cc_tuple = db.query_unparsed_data(condition)
            parsed_card = CreditCard.init_from_str_tuple(cc_tuple)
            credit_cards.append(parsed_card)
            
for credit_card in credit_cards:
    print(credit_card)
    print("---" * 10)