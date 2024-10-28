from collections import defaultdict
from creditcard.enums import RewardUnit, PurchaseCategory
from creditcard.schemas import CreditCardSchema
from database.auth.user import Account
from database.auth.user import User
from database.teller.transactions import Transaction
from datetime import datetime, timedelta
from pydantic import TypeAdapter
from scipy.stats import gamma
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema
from typing import List, Tuple
import numpy as np
import teller.utils as teller_utils

def get_last_three_months():
    today = datetime.today()
    start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)  # 1st day of the month, three months ago
    return start_date, today

async def get_average_monthly_purchases_three_months(user: User, db: Session) -> Tuple[dict, float]:
    teller_client = teller_utils.Teller()
    accounts: List[Account] = await teller_client.get_list_enrollments_accounts(enrollments=user.enrollments, db=db)

    if len(accounts) == 0:
        print(f"[INFO] No accounts found for user {user.id}")
        return {}, 0

    start_date, end_date = get_last_three_months()
    category_totals = defaultdict(float)
    all_transactions: List[TransactionSchema] = []

    for account in accounts:
        transactions: List[Transaction] = []
        query = account.transactions.filter(
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
    avg_monthly_spend_per_category, total_avg_monthly_spend = await get_average_monthly_purchases_three_months(user, db)

    # Check if category is 'general' to use total spend
    if category == PurchaseCategory.GENERAL:
        scale_param = total_avg_monthly_spend / shape_param
        total_future_spend = gamma.rvs(shape_param, scale=scale_param, size=10000) * T

        # Probability calculation for total spend exceeding threshold
        prob_exceed = np.mean(total_future_spend > threshold)
    else:
        scale_param = total_avg_monthly_spend / shape_param
        total_future_spend = gamma.rvs(shape_param, scale=scale_param, size=10000) * T

        category_proportions = {cat: spend / total_avg_monthly_spend for cat, spend in avg_monthly_spend_per_category.items()}
        p_category = category_proportions.get(category, 0)
        category_future_spend = total_future_spend * p_category

        prob_exceed = np.mean(category_future_spend > threshold)

    print(f"Probability of spending over ${threshold} in '{category}' over {T} months: {prob_exceed:.2%}")
    return prob_exceed

async def calculate_incremental_spending_probabilities(user, db, category, levels, T=3, shape_param=2):
    avg_monthly_spend_per_category, total_avg_monthly_spend = await get_average_monthly_purchases_three_months(user, db)

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
    previous_prob = 0
    for prob in cumulative_probs:
        incremental_prob = prob - previous_prob
        incremental_probs.append(max(0, incremental_prob))  # Ensure non-negative
        previous_prob = prob

    # Return a list of (level, incremental_prob)
    return list(zip(levels, incremental_probs))

async def compute_user_card_sign_on_bonus_value(user: User, db: Session, card: CreditCardSchema):
    total = 0
    for sign_on_bonus in card.sign_on_bonus:
        prob: float = await calculate_spending_probability(
            user=user,
            db=db,
            category=sign_on_bonus.purchase_type,
            threshold=sign_on_bonus.condition_amount,
            T=sign_on_bonus.get_timeframe_in_months()
        )
        total += prob * sign_on_bonus.reward_amount * RewardUnit.get_value(sign_on_bonus.reward_type)

    return total
