from database.creditcard.creditcard import CreditCard
from database.scrapes.cardratings import CardratingsScrape
from sqlalchemy.orm import Session
from typing import List

def create_credit_card(db: Session, cc : CreditCard) -> CreditCard:
    db.add(cc)
    db.commit()
    db.refresh(cc)
    return cc 

def create_cardratings_scrape(db: Session, cc_scrape : CardratingsScrape) -> CardratingsScrape:
    db.add(cc_scrape)
    db.commit()
    db.refresh(cc_scrape)
    return cc_scrape

     
def get_credit_card(db: Session, uid: str):
    return db.query(CreditCard).filter(CreditCard.uid == uid).first()

def get_all_credit_cards(db: Session) -> List[CreditCard]:
    return db.query(CreditCard).all()

# get the first n credit cards
def get_cardratings_scrapes(db: Session, n : int) -> List[CardratingsScrape]:
    return db.query(CardratingsScrape).limit(n).all()