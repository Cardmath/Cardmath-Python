from database.creditcard import CreditCard
from sqlalchemy.orm import Session
from typing import List

def get_all_credit_cards(db: Session) -> List[CreditCard]:
    return db.query(CreditCard).all()