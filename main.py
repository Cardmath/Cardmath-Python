from creditcard import CreditCard
from scrape import get_card_dict
from database.sqlite_impl import SQLiteImpl
from database.dbinterface import DatabaseInterface

import pandas as pd

CARDRATNGS_PAGE_DOWNLAOD = '../cardratings/cardratings.html'

def populate_database(cc_dict, db: DatabaseInterface):
    for idx, ((name, issuer, score_needed, description_used), card_attributes) in enumerate(cc_dict.items()):
        db.update_unparsed_data_table_entry(idx, name, issuer, score_needed, card_attributes, description_used)
    
def main():

    max_num_card = 5
    db = SQLiteImpl()
    db.connect('creditcards.db')
    db.create_unparsed_data_table()
    credit_cards = []

    if (db.is_empty()):
        cc_dict = get_card_dict(CARDRATNGS_PAGE_DOWNLAOD)
        populate_database(cc_dict, db)
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
    
if __name__ == "__main__":
    main()