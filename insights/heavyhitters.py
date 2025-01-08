from collections import defaultdict
from database.auth.user import Account
from database.auth.user import User, Onboarding
from typing import Union
from database.teller.transactions import Transaction
from insights.schemas import HeavyHittersRequest, HeavyHittersResponse, HeavyHitterSchema, MonthlyTimeframe, VENDOR_CONST, CATEGORY_CONST
from insights.utils import get_user_cc_eligible_transactions, CCEligibleTransactionsResponse
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema
from typing import List
from typing import Union

import creditcard.enums as enums
import teller.utils as teller_utils
import logging

class TwoPassHeavyHitters:
    def __init__(self, k, key=None, value=None):
        self.k = k
        self.keys = key if key is not None else lambda x: x  # Use identity function if key is not provided
        self.value = value if value is not None else lambda x: 1
        self.counters = {}  # Used for Misra-Gries in the first pass
        self.candidates = set()  # Candidate heavy hitters identified in the first pass

    def first_pass(self, stream):
        for item in stream:
            for key in self.keys(item):
                if not key:
                    continue
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
        
        # Accumulate exact counts for candidates
        for item in stream:
            for key in self.keys(item):
                if not key:
                    continue
                value = self.value(item)
                if key in self.candidates:
                    exact_counts[key] += value
        
        # TODO: Iterate over exact_counts, and if a vendor is present, remove the associated vendor value from the category total
        for key, value in list(exact_counts.items()):
            # Check if the key is a known vendor
            if key in {vendor.value for vendor in enums.Vendors}:
                # Get the associated category for the vendor
                category = enums.Vendors.get_category(key)
                
                # Subtract the vendor's count from the category total
                if category in exact_counts:
                    exact_counts[category] -= value
                else:
                    exact_counts[category] = -value  # Initialize with negative count if not present

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

async def read_heavy_hitters(db: Session, user : Union[User , Onboarding], request : HeavyHittersRequest) -> HeavyHittersResponse:
        teller_client = teller_utils.Teller() 
        accounts = None
        if isinstance(user, User):
            accounts: List[Account] = teller_client.get_list_enrollments_accounts(enrollments=user.enrollments, db=db)
        elif isinstance(user, Onboarding):
            accounts: List[Account] = teller_client.get_list_enrollments_accounts(enrollments=[user.enrollment], db=db)
        
        if not accounts or len(accounts) == 0:
            logging.warning(f"No accounts found for {type(user)}, {user.id}")
            return
        
        date_range = None
        if request.timeframe:
            date_range = (request.timeframe.start_month, request.timeframe.end_month)

        cc_eligible_txns_response: CCEligibleTransactionsResponse = get_user_cc_eligible_transactions(db, accounts, date_range)
        
        logging.debug(f"Found {len(cc_eligible_txns_response.transactions)} total transactions for user {user.email if isinstance(user, User) else user.emails}.")
        hh_two_pass = TwoPassHeavyHitters(k=200, key=get_transaction_category_and_vendor, value=get_transaction_amount)
        hh: dict[str, tuple] = hh_two_pass.heavy_hitters(cc_eligible_txns_response.transactions)

        out_hh = []
        categories = 0
        vendors = 0
        for hh, (percent, amount) in hh.items():
            logging.debug(f"Heavy Hitter: {hh}, percent: {percent}, amount: {amount}")
            if hh in {vendor.value for vendor in enums.Vendors}:
                out_hh.append(HeavyHitterSchema(type=VENDOR_CONST, name=hh, category=enums.Vendors.get_category(hh), percent=percent, amount=amount))
                vendors += 1
            elif hh in {category.value for category in enums.PurchaseCategory}:
                out_hh.append(HeavyHitterSchema(type=CATEGORY_CONST, category=hh, percent=percent, amount=amount))
                categories += 1
        logging.debug(f"[INFO] Found {vendors} vendors and {categories} categories in heavy hitters.")  
        return HeavyHittersResponse(heavyhitters=out_hh, timeframe=MonthlyTimeframe(start_month=cc_eligible_txns_response.oldest_date, end_month=cc_eligible_txns_response.newest_date), categorization_progress_summary=cc_eligible_txns_response.categorization_progress_summary)

def get_transaction_category_and_vendor(transaction: Union[Transaction, TransactionSchema]) -> Union[tuple[enums.Vendors, enums.PurchaseCategory], enums.PurchaseCategory]:
    transaction = TransactionSchema.model_validate(transaction)
    vendor = TransactionSchema.get_vendor(transaction)

    if vendor == enums.Vendors.UNKNOWN:
        return None, transaction.details.category
    
    return vendor, transaction.details.category

def get_transaction_amount(transaction: Union[Transaction, TransactionSchema]) -> float:
    return abs(transaction.amount)