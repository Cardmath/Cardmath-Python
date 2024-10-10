from sqlalchemy.orm import Session
from database.auth.user import Account
from database.teller.transactions import Transaction, Counterparty
from insights.schemas import HeavyHittersRequest, HeavyHittersResponse, HeavyHitterSchema, VENDOR_CONST, CATEGORY_CONST
from teller.schemas import AccountSchema
from typing import List
from database.auth.user import User
import teller.utils as teller_utils
from collections import defaultdict


class TwoPassHeavyHitters:
    def __init__(self, k, key=None, value=None):
        """
        Initializes the Two-Pass Heavy Hitters algorithm using Misra-Gries in the first pass.
        
        Parameters:
            k (int): Number of heavy hitters to track in the first pass. This corresponds to 
                     the reciprocal of the desired frequency threshold.
                     For example, for 0.25% heavy hitters, k should be set to 400.
        """
        self.k = k
        self.key = key if key is not None else lambda x: x  # Use identity function if key is not provided
        self.counters = {}  # Used for Misra-Gries in the first pass
        self.candidates = set()  # Candidate heavy hitters identified in the first pass

    def first_pass(self, stream):
        """
        First pass: Use Misra-Gries to find candidate heavy hitters.
        
        Parameters:
            stream (iterable): The input data stream to process.
        """
        for item in stream:
            key = self.key(item)  # Extract key from item
            if key in self.counters:
                self.counters[key] += 1
            elif len(self.counters) < self.k - 1:
                self.counters[key] = 1
            else:
                # Decrease count of all current counters
                for dict_key in list(self.counters.keys()):
                    self.counters[dict_key] -= 1
                    if self.counters[dict_key] == 0:
                        del self.counters[dict_key]
        
        # Identify candidate heavy hitters after the first pass
        self.candidates = set(self.counters.keys())

    def second_pass(self, stream):
        """
        Second pass: Count the exact frequencies of the candidate heavy hitters.
        
        Parameters:
            stream (iterable): The input data stream to process again.
        
        Returns:
            dict: Exact frequencies of the candidate heavy hitters.
        """
        exact_counts = defaultdict(int)
        for item in stream:
            key = self.key(item)  # Extract key from item
            if key in self.candidates:
                exact_counts[key] += 1
        return exact_counts

    def heavy_hitters(self, stream, total_items):
        """
        Finds heavy hitters with exact counts in two passes over the data.
        
        Parameters:
            stream (iterable): The input data stream to process.
            total_items (int): Total number of items in the data stream.
        
        Returns:
            dict: A dictionary with heavy hitters and their exact frequencies.
        """
        # First pass: Identify candidate heavy hitters
        self.first_pass(stream)
        
        # Second pass: Get exact frequencies of candidates
        exact_counts = self.second_pass(stream)
        
        # Return elements whose frequency is above the threshold
        threshold = total_items / self.k
        return {item: round(count / total_items, 2) for item, count in exact_counts.items() if count >= threshold}

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
                print(account)
                transactions: List[Transaction] = account.transactions.all()       
            elif account.id in request.account_ids :
                transactions: List[Transaction] = account.transactions.all()
            
            if len(transactions) == 0:
                print(f"[WARNING] No transactions found for account {account.id}")
            else :
                print(f"[INFO] Found {len(transactions)} transactions for account {account.id}")
            
            all_transactions.extend(transactions)

        hh_categories_two_pass = TwoPassHeavyHitters(k=25, key=get_transaction_category)
        hh_categories: dict[str, float] = hh_categories_two_pass.heavy_hitters(all_transactions, len(all_transactions))
        del hh_categories_two_pass  # Free memory
        hh_counterparties_two_pass = TwoPassHeavyHitters(k=100, key=get_transaction_counterparty_id)
        hh_counterparties_ids: dict[int, float] = hh_counterparties_two_pass.heavy_hitters(all_transactions, len(all_transactions))
        del hh_counterparties_two_pass  # Free memory

        # find the vendor categories and names with the id
        hh_vendors: List[Counterparty] = db.query(Counterparty).filter(Counterparty.id.in_(hh_counterparties_ids.keys())).all() 
        hh_vendors_category_dict: dict = {vendor.id: (vendor.name, vendor.transaction_details[0].category) for vendor in hh_vendors}

        out_vendors = []
        for hh_counterparty_id, percent in hh_counterparties_ids.items():
            name, category = hh_vendors_category_dict[hh_counterparty_id]
            if category is not None:
                out_vendors.append(HeavyHitterSchema(type=VENDOR_CONST, name=name, category=category, percent=percent))
            else:
                out_vendors.append(HeavyHitterSchema(type=VENDOR_CONST, name=name, category=None, percent=percent))

        out_categories = []
        for hh_category, percent in hh_categories.items():
            out_categories.append(HeavyHitterSchema(type=CATEGORY_CONST, category=hh_category, percent=percent))

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