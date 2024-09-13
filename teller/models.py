from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from database.teller.identity import Account
from database.teller.transactions import Transaction, TransactionDetails, Counterparty
from pydantic import BaseModel
from typing import List

TransactionModel = sqlalchemy_to_pydantic(Transaction, exclude=["self_link", "account_link", "details_id"])
TransactionDetailsModel = sqlalchemy_to_pydantic(TransactionDetails, exclude=["id", "counterparty_id"])
CounterpartyModel = sqlalchemy_to_pydantic(Counterparty, exclude=["id"])
AccountModel = sqlalchemy_to_pydantic(Account)
