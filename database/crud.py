from . import models
from sqlalchemy.orm import Session
import schemas

def create_credit_card(db: Session, cc : models.CreditCard) -> bool:
    try: 
        db.add(cc)
        db.commit()
        db.refresh(cc)
        return True
    except: 
        return False
     

def get_credit_card(db: Session, uid: str):
    return db.query(models.CreditCard).filter(models.CreditCard.uid == uid).first()

def get_all_credit_cards(db: Session):
    return db.query(models.CreditCard).all()

def get_all_cardratings_scrapes(db: Session):
    return db.query(models.CardratingsScrape).all()

# TODO Implement this function
def create_cardratings_scrape(db: Session, cc : schemas.CreditCardCreate) -> bool:
    return True