from collections import defaultdict
from creditcard.enums import PurchaseCategory
from database.auth.user import Account
from database.auth.user import User, Onboarding
from database.teller.transactions import Transaction
from datetime import datetime, timedelta
from insights.cache_context import CacheContext 
from pydantic import TypeAdapter
from scipy.stats import gamma
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema
from typing import List, Tuple, Union

import numpy as np
import teller.utils as teller_utils

def get_last_three_months():
    today = datetime.today()
    start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)  # 1st day of the month, three months ago
    return start_date, today

async def get_average_monthly_purchases_three_months(user: Union[User, Onboarding], db: Session) -> Tuple[dict, float]:
    teller_client = teller_utils.Teller()
    accounts = []
    if isinstance(user, User):
        accounts: List[Account] = teller_client.get_list_enrollments_accounts(enrollments=user.enrollments, db=db)
    elif isinstance(user, Onboarding):
        accounts: List[Account] = teller_client.get_enrollment_accounts(enrollment=user.enrollment, db=db)
    else:
        raise Exception(f"User is not of type User or Onboarding. Type: {type(user)}")

    if len(accounts) == 0:
        print(f"[INFO] No accounts found for user {user.id}")
        return {}, 0

    start_date, end_date = get_last_three_months()
    category_totals = defaultdict(float)
    all_transactions: List[TransactionSchema] = []

    for account in accounts:
        transactions: List[Transaction] = []
        query = db.query(Transaction).filter(
            Transaction.account_id == account.id,
            Transaction.type.notin_(["ach", "transfer", "withdrawal", "atm", "deposit", "wire", "interest", "digital_payment"]),
            Transaction.date.between(start_date, end_date)
        )
        transactions = query.all()
        if len(transactions) == 0:
            print(f"[WARNING] No transactions found for account {account.id}")
        else:
            print(f"[INFO] Found {len(transactions)} transactions for account {account.id}")

        all_transactions.extend(TypeAdapter(List[TransactionSchema]).validate_python(transactions))

        for transaction in transactions:
            category_totals[transaction.details.category] += abs(transaction.amount)

    avg_monthly_spend_per_category = {category: total / 3 for category, total in category_totals.items()}
    total_avg_monthly_spend = sum(category_totals.values()) / 3

    return avg_monthly_spend_per_category, total_avg_monthly_spend

async def calculate_spending_probability(user, db, category, threshold, T=3, shape_param=2):
    cache = CacheContext.get_cache()
    # Fix: Pass the compute function to get_cached_purchases
    avg_monthly_spend_per_category, total_avg_monthly_spend = await cache.get_cached_purchases(
        user, 
        db,
        compute_func=get_average_monthly_purchases_three_months
    )
    # Rest of your existing function remains the same
    if category == PurchaseCategory.GENERAL:
        scale_param = total_avg_monthly_spend / shape_param
        total_future_spend = gamma.rvs(shape_param, scale=scale_param, size=10000) * T
        prob_exceed = np.mean(total_future_spend > threshold)
    else:
        scale_param = total_avg_monthly_spend / shape_param
        total_future_spend = gamma.rvs(shape_param, scale=scale_param, size=10000) * T
        category_proportions = {cat: spend / total_avg_monthly_spend for cat, spend in avg_monthly_spend_per_category.items()}
        p_category = category_proportions.get(category, 0)
        category_future_spend = total_future_spend * p_category
        prob_exceed = np.mean(category_future_spend > threshold)

    return prob_exceed

async def calculate_incremental_spending_probabilities(user, db, category, levels, T=3, shape_param=2):
    cache = CacheContext.get_cache()
    avg_monthly_spend_per_category, total_avg_monthly_spend = await cache.get_cached_purchases(
        user, 
        db,
        compute_func=get_average_monthly_purchases_three_months
    )

    if category == PurchaseCategory.GENERAL.value:
        scale_param = total_avg_monthly_spend / shape_param
        total_future_spend = gamma.rvs(shape_param, scale=scale_param, size=10000) * T

        cumulative_probs = []
        for level in levels:
            prob = np.mean(total_future_spend >= level)
            cumulative_probs.append(prob)
    else:
        scale_param = total_avg_monthly_spend / shape_param
        total_future_spend = gamma.rvs(shape_param, scale=scale_param, size=10000) * T

        category_proportions = {cat: spend / total_avg_monthly_spend for cat, spend in avg_monthly_spend_per_category.items()}
        p_category = category_proportions.get(category, 0)
        category_future_spend = total_future_spend * p_category

        cumulative_probs = []
        for level in levels:
            prob = np.mean(category_future_spend >= level)
            cumulative_probs.append(prob)

    # Compute incremental probabilities
    incremental_probs = []
    previous_prob = 1
    for prob in cumulative_probs:
        incremental_prob = previous_prob - prob 
        incremental_probs.append(max(0, incremental_prob))  # Ensure non-negative
        previous_prob = prob
    
    return list(zip(levels, incremental_probs))

