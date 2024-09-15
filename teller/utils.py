from dotenv import load_dotenv
from teller.schemas import TransactionSchema
from pydantic import BaseModel
import os
from typing import List
import requests

TELLER_API_ENTRYPOINT = "https://api.teller.io/"
TELLER_ACCOUNTS = TELLER_API_ENTRYPOINT + "accounts"
TRANSACTIONS = "transactions"

class Teller(BaseModel):
    cert : str
    cert_key: str
    
    def get_transactions(self, account_id : str, auth_token : str) -> List[TransactionSchema]:
        uri = f"{TELLER_ACCOUNTS}/{account_id}/{TRANSACTIONS}"
        response = requests.get(uri, auth=(auth_token, ""), cert=(self.cert, self.cert_key))
        if response.status_code == 200:
            transactions = response.json()
            parsed_transactions = [TransactionSchema.model_validate(transaction) for transaction in transactions]           
            return parsed_transactions
        else:
            print(f"Error getting transactions: {response.status_code}")
            return []
    
load_dotenv()
client = Teller(cert=os.getenv("TELLER_CERT", "your_teller_cert"), cert_key=os.getenv("TELLER_CERT_KEY", "your_teller_cert_key"))
client.get_transactions("acc_p3oog0ncgd0ho7vl7q000", "token_lyrmqden5d4dnxujmnoo3jhibi")