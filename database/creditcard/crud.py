from database.creditcard.creditcard import CreditCard
from creditcard.schemas import CreditCardSchema
from database.creditcard.source import CreditCardSource
from sqlalchemy.orm import Session
from typing import List

def get_all_credit_cards(db: Session) -> List[CreditCard]:
    return db.query(CreditCard).all()