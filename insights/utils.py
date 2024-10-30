from insights.schemas import MonthlyTimeframe, OptimalCardsAllocationSolution

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
