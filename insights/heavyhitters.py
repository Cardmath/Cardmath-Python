from collections import defaultdict
from database.auth.user import Account
from database.auth.user import User
from database.teller.transactions import Transaction, Counterparty
from insights.schemas import HeavyHittersRequest, HeavyHittersResponse, HeavyHitterSchema, VENDOR_CONST, CATEGORY_CONST
from insights.schemas import MonthlyTimeframe
from pydantic import TypeAdapter
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema
from typing import List
from typing import Union
import creditcard.enums as enums
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
        return {item: ("{:.2f}%".format(round(amount / total, 4) * 100), amount) for item, amount in exact_amounts.items() if amount >= threshold}

async def read_heavy_hitters(db: Session, user : User, request : HeavyHittersRequest) -> HeavyHittersResponse:
        teller_client = teller_utils.Teller() 
        accounts: List[Account] = await teller_client.get_list_enrollments_accounts(enrollments=user.enrollments, db=db)
        
        start_date=None
        end_date = None
        if request.timeframe:
            start_date = request.timeframe.start_month
            end_date = request.timeframe.end_month

        if len(accounts) == 0:
            print(f"[INFO] No accounts found for user {user.id}")
            return HeavyHittersResponse(vendors=[], categories=[])
        
        
        all_transactions: List[TransactionSchema] = []
        for account in accounts:
            if request.account_ids != "all" and account.id not in request.account_ids:
                print(f"[INFO] Skipping account {account.id}")
                continue
            
            transactions: List[Transaction] = []
            if (request.account_ids == "all") or (account.id in request.account_ids):
                query = account.transactions.filter(Transaction.type.notin_(["ach", "transfer", "withdrawal", "atm", "deposit", "wire", "interest", "digital_payment"]))
                if request.timeframe:
                    query = query.filter(Transaction.date.between(request.timeframe.start_month, request.timeframe.end_month))
                if not start_date or not end_date:
                    start_date = query.order_by(Transaction.date.asc()).first().date
                    end_date = query.order_by(Transaction.date.desc()).first().date
                    query = query.filter(Transaction.date.between(start_date, end_date))
                transactions = query.all()
            if len(transactions) == 0:
                print(f"[WARNING] No transactions found for account {account.id}")
            else :
                print(f"[INFO] Found {len(transactions)} transactions for account {account.id}")
            
            all_transactions.extend(TypeAdapter(List[TransactionSchema]).validate_python(transactions))
        
        print(f"[INFO] Found {len(all_transactions)} total transactions.")
        hh_categories_two_pass = TwoPassHeavyHitters(k=100, key=get_transaction_category, value=get_transaction_amount)
        hh_categories: dict[str, tuple] = hh_categories_two_pass.heavy_hitters(all_transactions)
        hh_counterparties_two_pass = TwoPassHeavyHitters(k=100, key=get_transaction_counterparty_id, value=get_transaction_amount)
        hh_counterparties_ids: dict[int, tuple] = hh_counterparties_two_pass.heavy_hitters(all_transactions)

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
            print(f"Category: {hh_category}, percent: {percent}, amount: {amount}")
            if hh_category is not None:
                out_categories.append(HeavyHitterSchema(type=CATEGORY_CONST, category=hh_category, percent=percent, amount=amount))

        return HeavyHittersResponse(vendors=out_vendors, categories=out_categories, timeframe=MonthlyTimeframe(start_month=start_date, end_month=end_date))


def get_transaction_counterparty_id(transaction: Union[TransactionSchema, Transaction]):
    if not transaction.details:
        return None
    
    if isinstance(transaction, Transaction):
        return transaction.details.counterparty_id
    
    if isinstance(transaction, TransactionSchema):
        return transaction.details.counterparty.id
    
    return "no counterparty id" 
    
def get_transaction_category(transaction: Union[Transaction, TransactionSchema]):
    unknown = enums.PurchaseCategory.UNKNOWN.value
    if not transaction.details:
        return unknown

    if transaction.details.category:
        return transaction.details.category
    
    return unknown

def get_transaction_amount(transaction: Union[Transaction, TransactionSchema]) -> float:
    return abs(transaction.amount)