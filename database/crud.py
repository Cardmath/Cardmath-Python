from database.creditcard import CreditCard
from database.scrapes.cardratings import CardratingsScrape
from sqlalchemy.orm import Session
from typing import List

def create_credit_card(db: Session, cc : CreditCard) -> bool:
    try: 
        db.add(cc)
        db.commit()
        db.refresh(cc)
        return True
    except Exception as e: 
        print(e, "FAILED TO CREATE CREDIT CARD")
        return False
    
def create_cardratings_scrape(db: Session, cc_scrape : CardratingsScrape) -> bool:
    try: 
        db.add(cc_scrape)
        db.commit()
        db.refresh(cc_scrape)
        return True
    except Exception as e:
        print(e, "FAILED TO CREATE CARDRATINGS SCRAPE") 
        return False
     
def get_credit_card(db: Session, uid: str):
    return db.query(CreditCard).filter(CreditCard.uid == uid).first()

def get_all_credit_cards(db: Session) -> List[CreditCard]:
    return db.query(CreditCard).all()

# get the first n credit cards
def get_cardratings_scrapes(db: Session, n : int) -> List[CardratingsScrape]:
    return db.query(CardratingsScrape).limit(n).all()