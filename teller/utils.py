from auth.schemas import User
from database.auth import crud as user_crud
from database.auth.user import Enrollment, Account
from database.creditcard.creditcard import CreditCard
from database.teller.transactions import Transaction
from pydantic import BaseModel
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema, AccountSchema, GetTransactionsResponse
from typing import List
from typing import Union
import database.teller.crud as teller_crud 

import os
import requests

TELLER_API_ENTRYPOINT = "https://api.teller.io/"
TELLER_ACCOUNTS = TELLER_API_ENTRYPOINT + "accounts"
TRANSACTIONS = "transactions"
CREDIT_TYPE = "credit"
CREDIT_CARD_SUBTYPE = "credit_card"

## TODO TEST AND REFACTOR THIS METHOD
async def update_current_user_credit_cards(current_user: User, db: Session) -> List[Account]:
    out_cards : List[CreditCard] = []
    enrollments : List[Enrollment] = await read_current_user_enrollments(current_user, db)
    for enrollment in enrollments:
        accounts : List[Account] = await read_enrollment_accounts(enrollment, db)
        for account in accounts:
            credit_cards : List[CreditCard] = await get_account_credit_cards(account, db)
            out_cards.extend(credit_cards)
    
    await user_crud.update_user_with_credit_cards(db, out_cards, current_user.id)
    return out_cards

async def read_current_user_enrollments(current_user: User, db: Session) -> List[Enrollment]:
    enrollments : List[Enrollment] = db.query(Enrollment).filter(Enrollment.user_id == current_user.id).all()
    return enrollments

async def read_enrollment_accounts(enrollment: Enrollment, db: Session, schema=True) -> List[Account]:
    accounts : List[Account] = db.query(Account).filter(Account.enrollment_id == enrollment.enrollment_id).all()
    if (schema):
        return [AccountSchema.from_db(account) for account in accounts]
    return accounts

def is_credit_card_account(account: Account) -> bool:
    return account.type == CREDIT_TYPE and account.subtype == CREDIT_CARD_SUBTYPE

async def get_account_credit_cards(account: Account, db: Session) -> List[CreditCard]:
    is_credit_card = is_credit_card_account(account)    
    if not is_credit_card:
        print(f"[WARNING] Account {account.id} is not a credit card")
        return [] 
        
    return db.query(CreditCard).filter(CreditCard.name == account.name 
                                       and account.institution_name == CreditCard.issuer).all()

class Teller(BaseModel):
    cert: str = os.getenv("TELLER_CERT")
    cert_key: str = os.getenv("TELLER_CERT_KEY")
    
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
    
    async def get_enrollment_accounts(self, enrollment : Enrollment, db : Session) -> List[AccountSchema]: 
        enrollment_accounts_db : List[Account] = await read_enrollment_accounts(enrollment, db)
        if (enrollment_accounts_db is None or len(enrollment_accounts_db) == 0):
            enrollment_accounts : List[AccountSchema] = await self.fetch_enrollment_accounts(enrollment)
            for account in enrollment_accounts:
                teller_crud.create_account(db, account)
            return enrollment_accounts

        return [AccountSchema.from_db(account) for account in enrollment_accounts_db]

                    
    async def get_list_enrollments_accounts(self, db: Session, enrollments : List[Enrollment]) -> List[AccountSchema]:
        if enrollments is None:
            return []
        
        accounts: List[Account] = []
        for enrollment in enrollments:
            enrollment_accounts = await self.get_enrollment_accounts(enrollment, db)
            accounts.extend(enrollment_accounts)
        return accounts
    
    async def fetch_user_transactions(self, db: Session, current_user: User) -> List[Transaction]:
        user_enrollments : List[Enrollment] = await read_current_user_enrollments(current_user, db)
        fetched_transactions : List[Transaction] = []
        for enrollment in user_enrollments:
            transactions_temp = await self.get_enrollment_transactions(enrollment, db)
            if transactions_temp is not None:
                fetched_transactions.extend(transactions_temp)
        
        return GetTransactionsResponse(number=len(fetched_transactions))
        
    async def get_enrollment_transactions(self, enrollment: Enrollment, db: Session) -> List[Transaction]:
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
            teller_crud.create_transaction(db, parsed_transaction)
            out_transactions.append(parsed_transaction)
        return out_transactions
    
    async def fetch_transactions_from_list_account(self, accounts : List[Account], access_token : str, db : Session):
        out_transactions : List[Transaction] = []
        for account in accounts:
            fetched_transactions = await self.fetch_transactions_from_account(account, access_token, db)
            out_transactions.extend(fetched_transactions)
        return out_transactions