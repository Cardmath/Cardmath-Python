from auth.schemas import User
from database.auth.user import Enrollment, Account
from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema, AccountSchema
from typing import List
import database.teller.crud as teller_crud 
import os
import requests

TELLER_API_ENTRYPOINT = "https://api.teller.io/"
TELLER_ACCOUNTS = TELLER_API_ENTRYPOINT + "accounts"
TRANSACTIONS = "transactions"

# ONLY FETCHES THE FIRST ENROLLMENT 
def get_current_user_enrollment(current_user: User, db: Session) -> Enrollment:
    enrollment: Enrollment = db.query(Enrollment).filter(Enrollment.user_id == current_user.id).first()
    return enrollment

def get_enrollment_accounts(enrollment: Enrollment, db: Session) -> str:
    account: Account = db.query(Account).filter(Account.enrollment_id == enrollment.enrollment_id).first()
    return account

class Teller(BaseModel):
    cert: str = os.getenv("TELLER_CERT")
    cert_key: str = os.getenv("TELLER_CERT_KEY")
    
    def fetch(self, uri, access_token):
        return requests.get(uri, auth=(access_token, ""), cert=(self.cert, self.cert_key))
    
    def get_transactions(self, db: Session, current_user: User) -> List[TransactionSchema]:
        user_enrollment : Enrollment = get_current_user_enrollment(current_user, db)
        user_accounts : List[Account] = self.fetch_accounts(user_enrollment)
        
        for account in user_accounts:        
            teller_crud.create_account(db, account)
            uri = f"{TELLER_ACCOUNTS}/{account.id}/{TRANSACTIONS}"
            response = self.fetch(uri, user_enrollment.access_token)
            if response.status_code == 200:
                transactions = response.json()
                for transaction in transactions:
                    parsed_transaction = TransactionSchema.model_validate(transaction)
                    teller_crud.create_transaction(db, parsed_transaction)
                return transactions
            return []
        
    def fetch_accounts(self, enrollment : Enrollment) -> List[AccountSchema]:
        out_accounts : List[AccountSchema] = []
        response = self.fetch(TELLER_ACCOUNTS, enrollment.access_token)
        response = response.json()
        for account in response:
            out_accounts.append(AccountSchema.model_validate(account))
        return out_accounts
            