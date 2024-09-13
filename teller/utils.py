from pydantic import BaseModel
import requests
from models import TransactionModel, TransactionDetailsModel, CounterpartyModel
from dotenv import load_dotenv
import os

TELLER_API_ENTRYPOINT = "https://api.teller.io/"
TELLER_ACCOUNTS = TELLER_API_ENTRYPOINT + "accounts"
TRANSACTIONS = "transactions"

class Teller(BaseModel):
    cert : str
    cert_key: str
    
    def get_transactions(self, account_id : str, auth_token : str):
        uri = f"{TELLER_ACCOUNTS}/{account_id}/{TRANSACTIONS}"
        response = requests.get(uri, auth=(auth_token, ""), cert=(self.cert, self.cert_key))
        if response.status_code == 200:
            transactions = response.json()
            transaction_models = [TransactionModel(**transaction) for transaction in transactions]
            transaction_details_models = [TransactionDetailsModel(**transaction["details"]) for transaction in transactions]
            transaction_counterparty_models = [
                CounterpartyModel(**transaction["details"]["counterparty"])
                for transaction in transactions
                if transaction["details"].get("counterparty") is not None
            ]            
            print(transaction_models[-1]) 
            print(transaction_details_models[-1])
            print(transaction_counterparty_models[-1])
            return transaction_models
        else:
            return []
    
load_dotenv()
client = Teller(cert=os.getenv("TELLER_CERT"), cert_key=os.getenv("TELLER_CERT_KEY"))

client.get_transactions("PLACEHOLDER_ACCOUNT_ID", "PLACEHOLDER_AUTH_TOKEN")