from collections import defaultdict
from database.auth.user import Account
from database.auth.user import User
from database.teller.transactions import Transaction, Counterparty
from insights.schemas import HeavyHittersRequest, HeavyHittersResponse, HeavyHitterSchema, VENDOR_CONST, CATEGORY_CONST
from sqlalchemy.orm import Session
from typing import List
import teller.utils as teller_utils

class TwoPassHeavyHitters:
    def __init__(self, k, key=None, value=None):
        self.k = k
        self.key = key if key is not None else lambda x: x  # Use identity function if key is not provided
        self.value = value if value is not None else lambda x: 1
        self.counters = {}  # Used for Misra-Gries in the first pass
        self.candidates = set()  # Candidate heavy hitters identified in the first pass

    def first_pass(self, stream):
        for item in stream:
            key = self.key(item)  # Extract key from item
            value = self.value(item)  # Extract value from item
            if key in self.counters:
                self.counters[key] += value  # Increment by the item's value
            elif len(self.counters) < self.k - 1:
                self.counters[key] = value  # Initialize counter with the item's value
            else:
                # Decrease all counters by the current item's value
                to_remove = []
                for dict_key in self.counters:
                    self.counters[dict_key] -= value
                    if self.counters[dict_key] <= 0:
                        to_remove.append(dict_key)  # Mark for deletion

                # Remove keys with zero or negative counts
                for dict_key in to_remove:
                    del self.counters[dict_key]
        
        # Identify candidate heavy hitters after the first pass
        self.candidates = set(self.counters.keys())

    def second_pass(self, stream):
        exact_counts = defaultdict(int)
        for item in stream:
            key = self.key(item)  # Extract key from item
            value = self.value(item)   # Extract value from item
            if key in self.candidates:
                exact_counts[key] += value  # Accumulate the exact count for candidates
        return exact_counts

    def heavy_hitters(self, stream):
        # First pass: Identify candidate heavy hitters
        self.first_pass(stream)
        
        # Second pass: Get exact frequencies of candidates
        exact_amounts = self.second_pass(stream)
        
        # Calculate the total number of items in the stream (based on the values)
        total = sum(self.value(item) for item in stream)
        
        # Return elements whose frequency is above the threshold
        threshold = total / self.k
        return {item: (round(amount / total, 2), amount) for item, amount in exact_amounts.items() if amount >= threshold}

async def read_heavy_hitters(db: Session, user : User, request : HeavyHittersRequest) -> HeavyHittersResponse:
        teller_client = teller_utils.Teller() 
        accounts: List[Account] = await teller_client.get_list_enrollments_accounts(enrollments=user.enrollments, db=db)

        if len(accounts) == 0:
            print(f"[INFO] No accounts found for user {user.id}")
            return HeavyHittersResponse(vendors=[], categories=[])
        
        
        all_transactions = []
        for account in accounts:
            if request.account_ids != "all" and account.id not in request.account_ids:
                print(f"[INFO] Skipping account {account.id}")
                continue
            
            if request.account_ids == "all":
                transactions: List[Transaction] = account.transactions.all()       
            elif account.id in request.account_ids :
                transactions: List[Transaction] = account.transactions.all()
            
            if len(transactions) == 0:
                print(f"[WARNING] No transactions found for account {account.id}")
            else :
                print(f"[INFO] Found {len(transactions)} transactions for account {account.id}")
            
            all_transactions.extend(transactions)

        hh_categories_two_pass = TwoPassHeavyHitters(k=30, key=get_transaction_category)
        hh_categories: dict[str, tuple] = hh_categories_two_pass.heavy_hitters(all_transactions)
        del hh_categories_two_pass  # Free memory
        hh_counterparties_two_pass = TwoPassHeavyHitters(k=30, key=get_transaction_counterparty_id)
        hh_counterparties_ids: dict[int, tuple] = hh_counterparties_two_pass.heavy_hitters(all_transactions)
        del hh_counterparties_two_pass  # Free memory

        # find the vendor categories and names with the id
        hh_vendors: List[Counterparty] = db.query(Counterparty).filter(Counterparty.id.in_(hh_counterparties_ids.keys())).all() 
        hh_vendors_category_dict: dict = {vendor.id: (vendor.name, vendor.transaction_details[0].category) for vendor in hh_vendors}

        out_vendors = []
        for hh_counterparty_id, (percent, amount) in hh_counterparties_ids.items():
            name, category = hh_vendors_category_dict[hh_counterparty_id]
            if category is not None:
                out_vendors.append(HeavyHitterSchema(type=VENDOR_CONST, name=name, category=category, percent=percent, amount=amount))
            else:
                out_vendors.append(HeavyHitterSchema(type=VENDOR_CONST, name=name, category=None, percent=percent, amount=amount))

        out_categories = []
        for hh_category, (percent, amount) in hh_categories.items():
            out_categories.append(HeavyHitterSchema(type=CATEGORY_CONST, category=hh_category, percent=percent, amount=amount))

        return HeavyHittersResponse(vendors=out_vendors, categories=out_categories)


def get_transaction_counterparty_id(transaction: Transaction):
    if transaction.details and transaction.details.counterparty_id:
        return transaction.details.transaction.details.counterparty_id
    else:
        return None
    
def get_transaction_category(transaction: Transaction):
    if transaction.details and transaction.details.category:
        return transaction.details.category
    else:
        return None