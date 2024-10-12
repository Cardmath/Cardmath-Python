from auth.schemas import User
from database.auth import crud as user_crud
from database.auth.user import Enrollment, Account
from database.creditcard.creditcard import CreditCard
from database.teller import crud as teller_crud
from database.teller.transactions import Transaction
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema, AccountSchema
from typing import List, Union
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

import database.teller.crud as teller_crud 

import os
import requests

TELLER_API_ENTRYPOINT = "https://api.teller.io/"
TELLER_ACCOUNTS = TELLER_API_ENTRYPOINT + "accounts"
TRANSACTIONS = "transactions"
CREDIT_TYPE = "credit"
CREDIT_CARD_SUBTYPE = "credit_card"

## TODO TEST AND REFACTOR THIS METHOD
async def update_user_credit_cards(user: User, db: Session) -> List[Account]:
    '''
    Reads all of a user's accounts and determines which ones correspond to credit cards in our DB
    '''
    out_cards : List[CreditCard] = []
    enrollments : List[Enrollment] = await teller_crud.read_user_enrollments(user, db)
    for enrollment in enrollments:
        accounts : List[Account] = await read_enrollment_accounts(enrollment, db)
        for account in accounts:
            credit_cards : List[CreditCard] = await get_account_credit_cards(account, db)
            out_cards.extend(credit_cards)
    
    await user_crud.update_user_with_credit_cards(db, out_cards, user.id)
    return out_cards

async def read_user_new_enrollment(user: User, db: Session) -> Enrollment:
    '''
    Reads an arbitrary enrollment of the user from the DB that has been updated in the last 10 minutes
    '''
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    # TODO update this query to use the enrollment relationship with the user
    enrollments : List[Enrollment] = db.query(Enrollment).filter(Enrollment.user_id == user.id and Enrollment.last_updated >= ten_minutes_ago).first()
    return enrollments

async def read_enrollment_accounts(enrollment: Enrollment, db: Session) -> List[Account]:
    accounts : List[Account] = db.query(Account).filter(Account.enrollment_id == enrollment.enrollment_id).all()
    return accounts

def is_credit_card_account(account: Account) -> bool:
    return account.type == CREDIT_TYPE and account.subtype == CREDIT_CARD_SUBTYPE

async def get_account_credit_cards(account: Account, db: Session) -> List[CreditCard]:
    is_credit_card = is_credit_card_account(account)    
    if not is_credit_card:
        print(f"[INFO] Account {account.id} is not a credit card")
        return [] 
        
    return db.query(CreditCard).filter(CreditCard.name == account.name 
                                       and account.institution_name == CreditCard.issuer).all()

# TODO Optimize this query
async def read_enrollment_transactions(enrollment: Enrollment, db: Session) -> List[Transaction]:
    return db.query(Transaction).filter(Transaction.enrollment_id == enrollment.enrollment_id).all()

class Teller:
    def __init__(self):
        env_path = Path('/home/johannes/Cardmath/Cardmath-Python/.env')
        if env_path.exists():
            overriden = load_dotenv(dotenv_path=env_path, override=True)
            if overriden: print("[INFO] Loaded .env file.")
        else:
            print("[WARNING] .env file does not exist. Using environment variables.")
        self.cert = os.getenv("TELLER_CERT")
        self.cert_key = os.getenv("TELLER_CERT_KEY")
        if not self.cert or not self.cert_key:
            raise RuntimeError("could not find TLS certificate")

    async def fetch(self, uri, access_token):
        response = requests.get(uri, auth=(access_token, ""), cert=(self.cert, self.cert_key))
        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch {uri} from Teller API")
        return response
    async def fetch_enrollment_accounts(self, enrollment : Enrollment) -> List[AccountSchema]:
        response = await self.fetch(TELLER_ACCOUNTS, enrollment.access_token)
        response = response.json()
        
        out_accounts : List[AccountSchema] = []
        for account in response:
            out_accounts.append(AccountSchema.model_validate(account))
        return out_accounts
    
    async def get_enrollment_accounts(self, enrollment : Enrollment, db : Session) -> List[Account]: 
        enrollment_accounts_db : List[Account] = await read_enrollment_accounts(enrollment, db)
        if (enrollment_accounts_db and len(enrollment_accounts_db) > 0):
            return enrollment_accounts_db

        enrollment_accounts : List[AccountSchema] = await self.fetch_enrollment_accounts(enrollment)
        temp_accounts : List[Account] = []
        for account in enrollment_accounts:
            temp_account = await teller_crud.create_account(db=db, account=account)
            temp_accounts.append(temp_account)  
        return temp_accounts
                    
    async def get_list_enrollments_accounts(self, db: Session, enrollments : List[Enrollment]) -> List[Account]:
        if enrollments is None:
            return []
        
        accounts: List[Account] = []
        for enrollment in enrollments:
            enrollment_accounts = await self.get_enrollment_accounts(enrollment, db)
            accounts.extend(enrollment_accounts)
        return accounts
    
    async def fetch_user_transactions(self, db: Session, current_user: User) -> List[Transaction]:
        user_enrollments : List[Enrollment] = await teller_crud.read_user_enrollments(current_user, db)
        fetched_transactions : List[Transaction] = []
        for enrollment in user_enrollments:
            transactions_temp = await self.fetch_enrollment_transactions(enrollment, db)
            if transactions_temp is not None:
                fetched_transactions.extend(transactions_temp)
        return fetched_transactions     
        
    async def fetch_enrollment_transactions(self, enrollment: Optional[Enrollment], db: Session) -> List[Transaction]:
        if enrollment is None:
            print("[WARNING] Enrollment is None")
            return []
        
        user_accounts : List[Account] = await self.get_enrollment_accounts(enrollment, db)
        
        out_transactions : List[Transaction] = []
        for account_schema in user_accounts:
            fetched_transactions = await self.fetch_transactions_from_account(account=account_schema, 
                                            access_token=enrollment.access_token,
                                            db=db)
            out_transactions.extend(fetched_transactions)
        return out_transactions
            
    async def fetch_transactions_from_account(self, account : Union[Account, AccountSchema], access_token : str, db : Session) -> List[TransactionSchema]:
        acc_id = None
        if isinstance(account, Account):
            acc_id = account.id
        elif isinstance(account, AccountSchema):
            acc_id = account.id
            account = db.query(Account).filter(Account.id == acc_id).first()
        else :
            raise TypeError("Invalid account type")
        
        uri = f"{TELLER_ACCOUNTS}/{acc_id}/{TRANSACTIONS}"
        response = await self.fetch(uri, access_token)
        if response.status_code != 200:
            raise Exception(response, "Failed to fetch transactions")

        transactions : dict = response.json()
        out_transactions = []
        for transaction in transactions:
            parsed_transaction : TransactionSchema = TransactionSchema.model_validate(transaction)
            teller_crud.create_transaction(db, account= account, transaction=parsed_transaction)
            out_transactions.append(parsed_transaction)
        return out_transactions
    
    async def fetch_transactions_from_list_account(self, accounts : List[Account], access_token : str, db : Session):
        out_transactions : List[Transaction] = []
        for account in accounts:
            fetched_transactions = await self.fetch_transactions_from_account(account, access_token, db)
            out_transactions.extend(fetched_transactions)
        return out_transactions