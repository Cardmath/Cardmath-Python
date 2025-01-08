from database.auth.user import User
from contextlib import contextmanager
from creditcard.endpoints.read_database import read_credit_cards_database, CreditCardsDatabaseRequest, CreditCardsDatabaseResponse
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    PrivateFormat,
    Encoding,
    NoEncryption
)
from cryptography.x509 import load_pem_x509_certificate
from database.auth import crud as user_crud
from database.auth.user import Enrollment, Account
from database.creditcard.creditcard import CreditCard
from database.teller import crud as teller_crud
from database.teller.transactions import Transaction
from datetime import datetime, timedelta
from insights.categorize import run_categorize_transactions_in_new_thread
from requests_toolbelt.adapters.x509 import X509Adapter
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema, AccountSchema, TellerPaymentsAPIRequest
from typing import List, Union
from typing import Optional
import database.teller.crud as teller_crud 
import os

import random
import requests
import time


TELLER_API_ENTRYPOINT = "https://api.teller.io/"
TELLER_ACCOUNTS = TELLER_API_ENTRYPOINT + "accounts"
TRANSACTIONS = "transactions"
IDENTITY = TELLER_API_ENTRYPOINT + "identity"
CREDIT_TYPE = "credit"
CREDIT_CARD_SUBTYPE = "credit_card"

def update_user_credit_cards(user: User, db: Session) -> List[Account]:
    '''
    Reads all of a user's accounts and determines which ones correspond to credit cards in our DB
    '''
    environment = os.getenv('ENVIRONMENT', 'prod')  
        
    out_cards: List[CreditCard] = []
    enrollments: List[Enrollment] = teller_crud.read_user_enrollments(user, db)
    for enrollment in enrollments:
        accounts: List[Account] = read_enrollment_accounts(enrollment, db)
        for account in accounts:
            credit_cards: List[CreditCard] = []
            if environment == 'dev' and len(user.credit_cards) < 5: 
                response: CreditCardsDatabaseResponse = read_credit_cards_database(
                    request=CreditCardsDatabaseRequest(max_num=50, card_details="all", use_preferences=False),
                    db=db
                )
                if response.credit_card:
                    random_card = random.choice(response.credit_card).credit_card()
                    credit_cards = [random_card]
                    print(f"[DEVELOPMENT][INFO] assigned {random_card.name} to {account.name}")

            if environment == 'prod':
                credit_cards = get_account_credit_cards(account, db)
            
            out_cards.extend(credit_cards)
    
    user_crud.update_user_with_credit_cards(db, out_cards, user.id)
    return out_cards

def read_user_new_enrollment(user: User, db: Session) -> Enrollment:
    '''
    Reads an arbitrary enrollment of the user from the DB that has been updated in the last 10 minutes
    '''
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    enrollments = db.query(Enrollment).filter(
        (Enrollment.user_id == user.id) & (Enrollment.last_updated >= ten_minutes_ago)
    ).first()
    return enrollments

def read_enrollment_accounts(enrollment: Enrollment, db: Session) -> List[Account]:
    accounts: List[Account] = db.query(Account).filter(Account.enrollment_id == enrollment.id).all()
    return accounts

def is_credit_card_account(account: Account) -> bool:
    return account.type == CREDIT_TYPE and account.subtype == CREDIT_CARD_SUBTYPE

def get_account_credit_cards(account: Account, db: Session) -> List[CreditCard]:
    is_credit_card = is_credit_card_account(account)    
    if not is_credit_card:
        print(f"[INFO] Account {account.id} is not a credit card")
        return [] 
        
    return db.query(CreditCard).filter(
        (CreditCard.name == account.name) & 
        (account.institution_name == CreditCard.issuer)
    ).all()

class Teller:
    def __init__(self):
        cert = os.getenv("TELLER_CERT", "").encode("utf-8")
        if not cert:
            raise RuntimeError("TELLER_CERT environment variable is missing or empty.")
        try:
            cert = load_pem_x509_certificate(data=cert)
            cert_bytes = cert.public_bytes(encoding=Encoding.PEM)
        except Exception as e:
            raise RuntimeError(f"Invalid or incompatible certificate format: {str(e)}")
        
        key = os.getenv("TELLER_CERT_KEY", "").encode("utf-8")
        if not key:
            raise RuntimeError("TELLER_CERT_KEY environment variable is missing or empty.")
        try:
            key = load_pem_private_key(key, password=None)
            key_bytes = key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.PKCS8,
                encryption_algorithm=NoEncryption()
            )
        except Exception as e:
            raise RuntimeError(f"Invalid or incompatible private key format: {str(e)}")
        
        adapter = X509Adapter(
            max_retries=3,
            cert_bytes=cert_bytes,
            pk_bytes=key_bytes,
        )
        self.session = requests.Session()
        self.session.mount('https://api.teller.io/', adapter=adapter)
        
        self._validate_tls_config()

    def _validate_tls_config(self):
        """
        Validates the TLS setup by performing a test handshake with Teller.
        """
        test_url = "https://api.teller.io/"  # Use the full URL
        try:
            response = self.session.get(url=test_url, verify=False)
            response.raise_for_status()
            print("TLS handshake and connection succeeded.")
        except requests.exceptions.SSLError as ssl_error:
            raise RuntimeError(f"TLS handshake failed: {ssl_error}")
        except requests.exceptions.HTTPError as http_error:
            raise RuntimeError(f"HTTP error during handshake: {http_error}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during TLS handshake: {str(e)}")

    def fetch(self, path: str, token: str) -> requests.Response:
        response = self.session.get(path, auth=(token, ''), verify=False) # Figure out how to stop using verify=False cuz its sorta dangerous
        response.raise_for_status()
        return response
    
    def post(self,path: str, token: str, json: dict) -> requests.Response:
        response = self.session.post(path, auth=(token, ''), verify=False, json=json)
        response.raise_for_status()
        return response
    
    def options(self, path: str, token: str) -> requests.Response:
        response = self.session.options(path, auth=(token, ''), verify=False) # Figure out how to stop using verify=False cuz its sorta dangerous
        response.raise_for_status()
        return response

    def fetch_enrollment_accounts(self, enrollment: Enrollment) -> List[AccountSchema]:
        response = self.fetch(TELLER_ACCOUNTS, enrollment.access_token)
        response = response.json()
        print(f"[INFO] Fetched {len(response)} accounts from Teller API")
        
        out_accounts: List[AccountSchema] = []
        for account in response:
            out_accounts.append(AccountSchema.model_validate(account))
        return out_accounts
    
    def get_enrollment_accounts(self, enrollment: Enrollment, db: Session) -> List[Account]: 
        enrollment_accounts_db = read_enrollment_accounts(enrollment, db)
        if enrollment_accounts_db and len(enrollment_accounts_db) > 0:
            return enrollment_accounts_db

        enrollment_accounts = self.fetch_enrollment_accounts(enrollment)
        temp_accounts: List[Account] = []
        for account in enrollment_accounts:
            temp_account = teller_crud.create_account(db=db, account=account)
            temp_accounts.append(temp_account)  
        return temp_accounts
    
    def account_supports_zelle(self, account: Account, accessToken: str) -> bool:
        response = self.options(f"{TELLER_ACCOUNTS}/{account.id}/payments", accessToken)
        response = response.json()
        return ('schemes' in response and 
            any(scheme.get('name') == 'zelle' for scheme in response['schemes']))

    def get_enrollment_zelle_accounts(self, enrollment: Enrollment, db: Session) -> List[Account]:
        accs: List[Account] = self.get_enrollment_accounts(enrollment=enrollment, db=db)
        return list(filter(lambda acc: self.account_supports_zelle(
            account=acc, 
            accessToken=enrollment.access_token
        ), accs))
    
    def initiate_subscription_zelle_payment(self, acc_id, accessToken: str, payment: TellerPaymentsAPIRequest) -> str:
        '''
        Returns a teller connect token for the user to verify the purchase
        '''
        response: requests.Response = self.post(f"{TELLER_ACCOUNTS}/{acc_id}/payments", token=accessToken, json=payment.model_dump())
        return response.json()
    
    def validate_payment(self, pid: str, acc_id: str, accessToken: str):
        response: requests.Response = self.fetch(f"{TELLER_ACCOUNTS}/{acc_id}/payments/{pid}", token=accessToken)
        return response.status_code == 200
    
    def get_list_enrollments_accounts(self, db: Session, enrollments: List[Enrollment]) -> List[Account]:
        if enrollments is None:
            return []
        
        accounts: List[Account] = []
        for enrollment in enrollments:
            enrollment_accounts = self.get_enrollment_accounts(enrollment, db)
            accounts.extend(enrollment_accounts)
        return accounts
    
    def fetch_user_transactions(self, db: Session, current_user: User) -> List[Transaction]:
        user_enrollments = teller_crud.read_user_enrollments(current_user, db)
        fetched_transactions: List[Transaction] = []
        for enrollment in user_enrollments:
            transactions_temp = self.fetch_enrollment_transactions(enrollment, db)
            if transactions_temp is not None:
                fetched_transactions.extend(transactions_temp)
        return fetched_transactions     

    def fetch_enrollment_transactions(
        self, 
        enrollment: Optional[Enrollment], 
        db: Session, 
        should_categorize: bool = False,
        bulk_mode: bool = True,
        batch_size: int = 150,
        is_new_user: bool = False
    ) -> List[Transaction]:
        if enrollment is None:
            print("[WARNING] Enrollment is None")
            return []
        
        user_accounts = self.get_enrollment_accounts(enrollment, db)
        
        out_transactions: List[Transaction] = []
        for account_schema in user_accounts:
            fetched_transactions = self.fetch_transactions_from_account(
                account=account_schema,
                access_token=enrollment.access_token,
                db=db,
                should_categorize=should_categorize,
                bulk_mode=bulk_mode,
                batch_size=batch_size,
                is_new_user=is_new_user  # Pass through the is_new_user flag
            )
            out_transactions.extend(fetched_transactions)
        return out_transactions
    
    @staticmethod
    @contextmanager
    def timer(description: str):
        start = time.perf_counter()
        yield
        elapsed = time.perf_counter() - start
        print(f"{description}: {elapsed:.2f} seconds")
    
    def fetch_transactions_from_account(
        self,
        account: Union[Account, AccountSchema],
        access_token: str,
        db: Session,
        should_categorize: bool = False,
        bulk_mode: bool = True,
        batch_size: int = 150,
        is_new_user: bool = False
    ) -> List[TransactionSchema]:
        with self.timer("Total transaction fetch and write"):
            # Handle account ID resolution
            acc_id = None
            if isinstance(account, Account):
                acc_id = account.id
            elif isinstance(account, AccountSchema):
                acc_id = account.id
                account = db.query(Account).filter(Account.id == acc_id).first()
            else:
                raise TypeError("Invalid account type of type: " + str(type(account)))
            
            print(f"Fetching transactions for account {acc_id}")
            
            # Fetch transactions from API
            with self.timer("API fetch"):
                uri = f"{TELLER_ACCOUNTS}/{acc_id}/{TRANSACTIONS}"
                response = self.fetch(uri, access_token)
                if response.status_code != 200:
                    raise Exception(response, "Failed to fetch transactions")
                transactions: dict = response.json()
            
            unknown_transactions = []
            with self.timer(f"Processing and writing {len(transactions)} transactions"):
                if bulk_mode:
                    # Process in optimized batches
                    for i in range(0, len(transactions), batch_size):
                        batch = transactions[i:i + batch_size]
                        print(f"[INFO] Processing batch {i//batch_size + 1} of {len(transactions)//batch_size + 1}")
                        
                        batch_unknown = []
                        parsed_batch = []
                        
                        # Parse all transactions in batch first
                        for transaction in batch:
                            parsed_transaction = TransactionSchema.model_validate(transaction)
                            if parsed_transaction.details.category in ["unknown", "general"] and should_categorize:
                                batch_unknown.append(parsed_transaction.txn_id)
                            parsed_batch.append(parsed_transaction)
                        
                        # Use bulk creation for the batch
                        created_transactions = teller_crud.create_transactions_bulk(
                            db, 
                            account=account, 
                            transactions=parsed_batch,
                            batch_size=batch_size,
                            is_new_user=is_new_user  # Pass through the optimization flag
                        )
                        
                        unknown_transactions.extend(batch_unknown)
                        print(f"[INFO] Committed batch {i//batch_size + 1}, "
                            f"{len(unknown_transactions)} unknown transactions so far")
                else:
                    # Original one-by-one processing
                    for idx, transaction in enumerate(transactions):
                        if idx % 25 == 0 and idx > 0:
                            print(f"[INFO] Processed {idx} transactions for account {acc_id}")
                        
                        parsed_transaction = TransactionSchema.model_validate(transaction)
                        
                        if parsed_transaction.details.category in ["unknown", "general"] and should_categorize:
                            unknown_transactions.append(parsed_transaction.txn_id)
                        
                        teller_crud.create_transaction(db, account=account, transaction=parsed_transaction)
            
            if unknown_transactions:
                with self.timer("Categorization"):
                    run_categorize_transactions_in_new_thread(unknown_transactions, 100)
            
            print(f"[INFO] Fetched {len(transactions)} transactions for account {acc_id}")

            return unknown_transactions
    
    def fetch_transactions_from_list_account(self, accounts: List[Account], access_token: str, db: Session):
        print(f"[INFO] Fetching transactions from {len(accounts)} accounts")
        out_transactions: List[Transaction] = []
        for account in accounts:
            fetched_transactions = self.fetch_transactions_from_account(account, access_token, db)
            out_transactions.extend(fetched_transactions)
        return out_transactions
    
    def fetch_identity(self, access_token):
        uri = f"{IDENTITY}"
        response = self.fetch(uri, access_token)
        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch {uri} from Teller API")
        return response