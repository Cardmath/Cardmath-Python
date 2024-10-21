from creditcard.enums import PurchaseCategory
from creditcard.utils.openai import structure_with_openai
from database.sql_alchemy_db import SyncSessionLocal
from database.teller.transactions import Transaction, TransactionDetails
from pydantic import BaseModel
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema
from typing import List

import asyncio
import json 
import threading

separator = "\n - "

class CategorizationElement(BaseModel):
    txn_id: str
    category: str

class BatchCategorizationResponse(BaseModel):
    categorizations: List[CategorizationElement]

# Function to run in a thread
def categorize_transactions_in_thread(txn_ids: List[int], batch_size: int):
    # Create a new session for this thread
    db: Session = SyncSessionLocal()

    try:
        # Call your categorize_transactions function with the session
        categorize_transactions(txn_ids=txn_ids, batch_size=batch_size, db=db)
    finally:
        # Ensure the session is closed when done
        db.close()
# Fire-and-forget thread without awaiting it# Fire-and-forget thread without awaiting it
def run_categorize_transactions_in_new_thread(txn_ids: List[int], batch_size: int):
    thread = threading.Thread(target=categorize_transactions_in_thread, args=(txn_ids, batch_size))
    thread.start()
def categorize_transactions(txn_ids: List[int], batch_size: int, db: Session) -> List[TransactionSchema]:
    # Fetch uncategorized transactions from the database
    uncategorized_transactions: List[Transaction] = db.query(Transaction).filter(Transaction.txn_id.in_(txn_ids)).all()

    # Extract valid transaction IDs
    valid_txn_ids = {transaction.txn_id for transaction in uncategorized_transactions}

    # Calculate the number of valid and invalid transaction IDs
    num_valid_txn_ids = len(valid_txn_ids)
    num_total_txn_ids = len(txn_ids)
    num_invalid_txn_ids = num_total_txn_ids - num_valid_txn_ids

    # Print summary of valid and invalid transaction IDs
    print(f"Total transaction IDs: {num_total_txn_ids}")
    print(f"Valid transaction IDs found in database: {num_valid_txn_ids}")
    print(f"Invalid transaction IDs not found in database: {num_invalid_txn_ids}")

    # Convert transactions to Pydantic schemas
    uncategorized_transactions_schemas: List[TransactionSchema] = [
        TransactionSchema.model_validate(transaction) for transaction in uncategorized_transactions
    ]

    # Split into batches of size at most batch_size
    schema_batches = [
        uncategorized_transactions_schemas[i:i + batch_size] 
        for i in range(0, len(uncategorized_transactions_schemas), batch_size)
    ]
    
    categorized_batches: List[BatchCategorizationResponse] = []
    for batch in schema_batches:
        categorized_batch = categorize_batch(batch)
        categorized_batches.append(categorized_batch)

    # Flatten the categorized batches into a single list of categorized transactions
    categorized_transactions: List[CategorizationElement] = [
        txn for batch in categorized_batches for txn in batch.categorizations
    ]

    # Prepare update data, but only include transactions with valid IDs
    update_data = [
        {
            'txn_id': txn.txn_id,
            'category': txn.category 
        }
        for txn in categorized_transactions if txn.txn_id in valid_txn_ids
    ]

    # Count how many valid transactions are being updated
    num_transactions_to_update = len(update_data)

    # Perform bulk update for valid transactions
    db.bulk_update_mappings(TransactionDetails, update_data)

    # Commit the session
    db.commit()
    print(f"{num_transactions_to_update} transactions were updated successfully.")

def categorize_batch(batch_transactions: List[TransactionSchema]) -> BatchCategorizationResponse:
    prompt = batch_categorization_prompt(batch_transactions)
    
    return asyncio.run(structure_with_openai(
        prompt=prompt, 
        response_format=batch_categorization_response_format(), 
        schema=BatchCategorizationResponse
    ))

def batch_categorization_response_format() -> dict:
    enum_category = json.dumps([purchase_category.value for purchase_category in PurchaseCategory], ensure_ascii=False)

    return {
        "type": "json_schema",
        "json_schema": {
            "name": "reward_category_map_response",
            "schema": {
                "type": "object",
                "properties": {
                    "categorizations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "txn_id": {"type": "string"},
                                "category": {"type": "string", "enum": json.loads(enum_category)},
                            },
                            "required": ["txn_id", "category"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["categorizations"],
                "additionalProperties": False
            }
        }
    }

def batch_categorization_prompt(transactions: List[TransactionSchema]) -> str:
    return f'''You are operating in a data understanding pipeline. 
    You are being given a list of transactions in json format and you need to categorize them.
    Your goal is to output a list of json objects of the form (txn_id, category).
    You should preserve the order of the outputs with respect to the order of the input transactions.
    Very important: make sure the txn_id for your categorization is the same as the txn_id in the input list.

    Now I will start with the list of transactions that you should analyze:
    {separator.join([str(transaction) for transaction in transactions])}
    '''
