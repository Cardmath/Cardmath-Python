from insights.schemas import MonthlyTimeframe, OptimalCardsAllocationSolution, CategorizationProgressSummary
from database.auth.user import Account
from typing import List, Optional, Tuple, Dict
from database.teller.transactions import Transaction
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Query    

import datetime

def remove_duplicates_ordered(lst):
    seen = set()
    return [x for x in lst if x not in seen and not seen.add(x)]

def months_between(start_date: datetime.date, end_date: datetime.date) -> int:
    return (end_date.year - start_date.year) * 12 + end_date.month - start_date.month + 1

def calculate_timeframe_years(timeframe: MonthlyTimeframe) -> int:
    total_months = months_between(timeframe.start_month, timeframe.end_month)
    return max(1, total_months // 12)

def calculate_timeframe_months(timeframe: MonthlyTimeframe) -> int:
    return months_between(timeframe.start_month, timeframe.end_month)

def hamming_distance(sol1: OptimalCardsAllocationSolution, sol2: OptimalCardsAllocationSolution) -> int:
    # Compare total_reward_allocation fields or other relevant aspects
    return sum(1 for x, y in zip(sol1.total_reward_allocation, sol2.total_reward_allocation) if x != y)

class CCEligibleTransactionsResponse(BaseModel):
    transactions: List[Transaction]
    oldest_date: Optional[datetime.date]
    newest_date: Optional[datetime.date]
    categorization_progress_summary: CategorizationProgressSummary

    model_config = ConfigDict(arbitrary_types_allowed=True)

def get_user_cc_eligible_transactions(accounts: List[Account], date_range: Optional[Tuple[str, str]] = None) -> CCEligibleTransactionsResponse:
    """
    Retrieve credit card eligible transactions for a user's accounts using the specified filter.
    """
    ineligible_types = ["ach", "transfer", "withdrawal", "atm", "deposit", "wire", "interest", "digital_payment"]
    all_transactions = []
    categorized_cc_eligible_count = 0
    uncategorized_cc_eligible_count = 0
    non_cc_eligible_count = 0

    for account in accounts:
        # Filter out ineligible transactions
        query: Query = account.transactions

        if date_range:
            query = query.filter(Transaction.date.between(date_range[0], date_range[1]))

        account_transactions = query.all()

        for transaction in account_transactions:
            transaction_category = transaction.details.category if transaction.details else None
            if transaction.type in ineligible_types:
                non_cc_eligible_count += 1
            elif transaction_category not in ["general", "unknown", None]:
                categorized_cc_eligible_count += 1
                all_transactions.append(transaction)
            elif transaction_category in ["general", "unknown", None]:
                uncategorized_cc_eligible_count += 1
                all_transactions.append(transaction)

    # Extract oldest and newest transaction dates
    if all_transactions:
        sorted_transactions = sorted(all_transactions, key=lambda t: t.date)
        oldest_date = sorted_transactions[0].date
        newest_date = sorted_transactions[-1].date
    else:
        oldest_date = None
        newest_date = None

    return CCEligibleTransactionsResponse(
        transactions=all_transactions,
        oldest_date=oldest_date,
        newest_date=newest_date,
        categorization_progress_summary=CategorizationProgressSummary(
            categorized_cc_eligible_count=categorized_cc_eligible_count,
            uncategorized_cc_eligible_count=uncategorized_cc_eligible_count,
            non_cc_eligible_count=non_cc_eligible_count
        )
    )