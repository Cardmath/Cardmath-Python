from auth.schemas import User
from database.auth.user import Enrollment, Account
from database.creditcard import CreditCard
from database.teller.transactions import Transaction
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
CREDIT_TYPE = "credit"
CREDIT_CARD_SUBTYPE = "credit card"

async def read_current_user_enrollments(current_user: User, db: Session) -> Enrollment:
    return db.query(Enrollment).filter(Enrollment.user_id == current_user.id).all()

async def read_enrollment_accounts(enrollment: Enrollment, db: Session) -> List[Account]:
    return db.query(Account).filter(Account.enrollment_id == enrollment.enrollment_id).all()

async def get_account_credit_cards(account: Account, db: Session) -> CreditCard:
    is_credit_card = account.type == CREDIT_TYPE and account.subtype == CREDIT_CARD_SUBTYPE
    
    if not is_credit_card:
        return [] 
        
    return db.query(CreditCard).filter(CreditCard.name == account.name 
                                       and account.institution_name == CreditCard.issuer).first()

class Teller(BaseModel):
    cert: str = os.getenv("TELLER_CERT")
    cert_key: str = os.getenv("TELLER_CERT_KEY")
    
    async def fetch(self, uri, access_token):
        return requests.get(uri, auth=(access_token, ""), cert=(self.cert, self.cert_key))
    
    async def fetch_enrollment_accounts(self, enrollment : Enrollment) -> List[AccountSchema]:
        out_accounts : List[AccountSchema] = []
        response = await self.fetch(TELLER_ACCOUNTS, enrollment.access_token)
        response = response.json()
        for account in response:
            out_accounts.append(AccountSchema.model_validate(account))
        return out_accounts
    
    async def get_enrollment_accounts(self, enrollment : Enrollment, db : Session) -> List[Account]: 
        if enrollment is None:
            return []
        
        enrollment_accounts : List[Account] = await read_enrollment_accounts(enrollment, db)
        if enrollment_accounts is None:
            enrollment_accounts : List[AccountSchema] = await self.fetch_enrollment_accounts(enrollment)
            enrollment_accounts : List[Account] = [teller_crud.create_account(db, account) for account in enrollment_accounts]
        return enrollment_accounts
            
    async def get_list_enrollments_accounts(self, db: Session, enrollments : List[Enrollment]) -> List[AccountSchema]:
        if enrollments is None:
            return []
        
        accounts: List[Account] = []
        for enrollment in enrollments:
            enrollment_accounts = await self.get_enrollment_accounts(enrollment, db)
            accounts.extend(enrollment_accounts)
        return accounts
    
    async def fetch_user_transactions(self, db: Session, current_user: User) -> List[TransactionSchema]:
        print("STARTED FETCH")
        user_enrollments : List[Enrollment] = await read_current_user_enrollments(current_user, db)
        print("USER ENROLLMENTS GOT")
        user_accounts : List[Account] = await self.get_list_enrollments_accounts(db, user_enrollments)
        print("USER ACCOUNTS GOT")
        fetched_transactions : List[Transaction] = await self.fetch_transactions_from_list_account(user_accounts, user_enrollments[0].access_token, db)
        print("TRANSACTIONS FETCHED")
        return fetched_transactions
        
    async def get_enrollment_transactions(self, enrollment: Enrollment, db: Session) -> List[Transaction]:
        user_accounts : List[Account] = await self.get_enrollment_accounts(enrollment, db)
        out_transactions : List[Transaction] = []
        for account_schema in user_accounts:
            account : Account = teller_crud.create_account(db, account_schema)  
            fetched_transactions = await self.fetch_transactions_from_account(account=account, 
                                            access_token=enrollment.access_token,
                                            db=db)
            out_transactions.extend(fetched_transactions)
            
    async def fetch_transactions_from_account(self, account : Account, access_token : str, db : Session) -> List[Transaction]:
        uri = f"{TELLER_ACCOUNTS}/{account.id}/{TRANSACTIONS}"
        response = await self.fetch(uri, access_token)
        if response.status_code == 200:
            transactions = response.json()
            out_transactions = []
            for transaction in transactions:
                parsed_transaction = TransactionSchema.model_validate(transaction)
                out_transactions.append(
                    teller_crud.create_transaction(db, parsed_transaction))
            return out_transactions
        return []
    
    async def fetch_transactions_from_list_account(self, accounts : List[Account], access_token : str, db : Session):
        out_transactions : List[Transaction] = []
        for account in accounts:
            fetched_transactions = await self.fetch_transactions_from_account(account, access_token, db)
            out_transactions.extend(fetched_transactions)
        return out_transactions