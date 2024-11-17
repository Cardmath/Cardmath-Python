from database.auth.user import Account, User
from database.teller.transactions import Transaction
from insights.schemas import MovingAveragesSeries, CategoriesMovingAveragesRequest, CategoriesMovingAveragesResponse
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema
from typing import List

import pandas as pd
import teller.utils as teller_utils
import logging

async def compute_categories_moving_averages(
    request: CategoriesMovingAveragesRequest, 
    user: User, 
    db: Session
) -> CategoriesMovingAveragesResponse:  

    # Initialize Teller client and fetch accounts
    teller_client = teller_utils.Teller() 
    accounts: List[Account] = await teller_client.get_list_enrollments_accounts(
        enrollments=user.enrollments, 
        db=db
    )

    if len(accounts) == 0:
        logging.warning(f"No accounts found for user {user.id}")
        return CategoriesMovingAveragesResponse(vendors=[], categories=[])

    # Initialize transaction list
    all_transactions: List[Transaction] = []

    for account in accounts:
        if request.account_ids != "all" and account.id not in request.account_ids:
            logging.debug(f"Skipping account {account.id}")
            continue

        query = account.transactions.filter(
            Transaction.type.notin_(["ach", "transfer", "withdrawal", "atm", "deposit", "wire", "interest", "digital_payment"])
        )
        
        if isinstance(request.date_range, tuple) and len(request.date_range) == 2:
            query = query.filter(Transaction.date.between(request.date_range[0], request.date_range[1]))

        query = query.filter(Transaction.status == "posted")

        account_transactions: List[Transaction] = query.all()
        
        if len(account_transactions) == 0:
            logging.warning(f"No transactions found for account {account.id}")
        else:
            logging.debug(f"Found {len(account_transactions)} transactions for account {account.id}")
        
        # Add to the aggregate list
        all_transactions.extend(account_transactions)

    # Parse the List of transactions into a pandas dataframe 
    df = pd.DataFrame([ TransactionSchema.model_validate(transaction).model_dump() for transaction in all_transactions])

    # Step 1: Filter transactions to only include the desired types
    df = df[df['type'].isin(['card_payment', 'digital_payment', 'bill_payment', 'fee'])]

    # Step 2: Extract category and date, and ensure 'date' is of datetime type
    df['category'] = df['details'].apply(lambda x: x['category'])
    df['date'] = pd.to_datetime(df['date'])

    # Step 3: Check for and remove duplicates based on 'category' and 'date'
    df = df.drop_duplicates(subset=['category', 'date'])

    # Step 4: Set date as index and sort by index to ensure chronological order
    df = df.set_index('date')
    df = df.sort_index()

    # Step 5: Define window size for rolling average
    window_size = 3  # Use a fixed window size or replace with `request.window_size`
    rolling_window = f'{window_size}D'  # Use a time-based offset for rolling

    # Step 6: Create an empty DataFrame to hold the results with consistent date range
    date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    results = pd.DataFrame({'date': date_range}).set_index('date')

    # Step 7: Calculate the moving average for each category and merge with the results DataFrame
    category_dfs = {}
    for category, group in df.groupby('category'):
        # Reindex each category group to include all dates in the range
        group = group.reindex(date_range, fill_value=0)  # Fill missing dates with 0
        group['category'] = category  # Add category back for reference

        # Calculate the rolling average on the 'amount' column using the specified window
        group['moving_average'] = group['amount'].rolling(window=rolling_window, min_periods=1).mean()

        # Store the group DataFrame for this category
        category_dfs[category] = group.reset_index()

    # Create a list of MovingAveragesSeries objects from the category DataFrames
    moving_averages_series = []
    for category, category_df in category_dfs.items():
        moving_averages_series.append(MovingAveragesSeries(name=category, moving_average=category_df['moving_average'].to_list()))

    # Return the results as a CategoriesMovingAveragesResponse
    logging.debug(f"Found {len(moving_averages_series)} categories")
    return CategoriesMovingAveragesResponse(dates=results.index.to_list(), categories=moving_averages_series)
