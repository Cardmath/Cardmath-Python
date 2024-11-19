import logging

from insights.schemas import (
    MonthlyTimeframe,
    OptimalCardsAllocationSolution,
    CategorizationProgressSummary,
)
from database.auth.user import Account
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from database.teller.transactions import Transaction
from pydantic import BaseModel, ConfigDict
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

def get_user_cc_eligible_transactions(
    db: Session,
    accounts: List[Account],
    date_range: Optional[Tuple[str, str]] = None,
) -> CCEligibleTransactionsResponse:
    """
    Retrieve credit card eligible transactions for a user's accounts using the specified filter.
    """
    ineligible_types = [
        "ach",
        "transfer",
        "withdrawal",
        "atm",
        "deposit",
        "wire",
        "interest",
        "digital_payment",
    ]
    all_transactions = []
    categorized_cc_eligible_count = 0
    uncategorized_cc_eligible_count = 0

    account_ids = [account.id for account in accounts]

    # Build the base query for all transactions
    total_transactions_query = db.query(Transaction).filter(Transaction.account_id.in_(account_ids))

    if date_range:
        start_date, end_date = date_range
        total_transactions_query = total_transactions_query.filter(
            Transaction.date.between(start_date, end_date)
        )

    # Fetch all transactions for the user
    total_transactions = total_transactions_query.all()
    total_transaction_count = len(total_transactions)

    # Build the query for eligible transactions by excluding ineligible types
    eligible_transactions_query = total_transactions_query.filter(
        ~Transaction.type.in_(ineligible_types)
    )

    # Fetch eligible transactions
    account_transactions = eligible_transactions_query.all()
    eligible_transaction_count = len(account_transactions)

    # Calculate the number of ineligible transactions
    non_cc_eligible_count = total_transaction_count - eligible_transaction_count

    # Add a logging warning if no ineligible transactions are found
    if non_cc_eligible_count == 0:
        logging.warning("No ineligible transactions found.")

    # Process eligible transactions
    for transaction in account_transactions:
        transaction_category = (
            transaction.details.category if transaction.details else None
        )
        if transaction_category not in ["general", "unknown", None]:
            categorized_cc_eligible_count += 1
            all_transactions.append(transaction)
        else:
            uncategorized_cc_eligible_count += 1
            all_transactions.append(transaction)

    # Determine the oldest and newest transaction dates
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
            non_cc_eligible_count=non_cc_eligible_count,
        ),
    )