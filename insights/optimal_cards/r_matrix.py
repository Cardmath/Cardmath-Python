from copy import deepcopy
from creditcard.endpoints.read_database import read_credit_cards_database, CreditCardsDatabaseRequest
from creditcard.enums import PurchaseCategory, RewardUnit
from creditcard.schemas import CreditCardSchema
from database.creditcard.creditcard import CreditCard
from fastapi import HTTPException
from database.auth.user import User
from insights.category_spending_prediction import calculate_incremental_spending_probabilities
from insights.heavyhitters import read_heavy_hitters, HeavyHittersRequest, HeavyHittersResponse
from insights.optimal_cards.matrix_helpers import create_cards_matrix, create_heavy_hitter_vector
from insights.schemas import OptimalCardsAllocationRequest, RMatrixDetails
from insights.utils import calculate_timeframe_years
from sqlalchemy.orm import Session

import numpy as np


async def compute_r_matrix(db: Session, user: User, request: OptimalCardsAllocationRequest) -> RMatrixDetails:
    heavy_hitters_response: HeavyHittersResponse = await read_heavy_hitters(
        db=db, user=user, request=HeavyHittersRequest(account_ids="all", timeframe=request.timeframe)
    )

    ccs_used = []
    ccs_added = []
    is_new_flags = []  # Keep track of whether each card is new

    if request.wallet_override:
        # Process wallet_override cards
        for idx, cc in enumerate(request.wallet_override.cards):
            # cc is an OptimalCardsAllocationCardLookupSchema
            # cc.card is a CardLookupSchema with 'name' and 'issuer'
            card_db = db.query(CreditCard).filter_by(name=cc.card.name, issuer=cc.card.issuer).first()
            if not card_db:
                raise HTTPException(status_code=400, detail=f"Credit card {cc.card.name} by {cc.card.issuer} not found.")
            card_schema = CreditCardSchema.model_validate(card_db)
            ccs_used.append(card_schema)
            
            if cc.is_new:
                is_new_flags.append(idx)
    else:
        held_cards = user.credit_cards
        ccs_used = [CreditCardSchema.model_validate(cc) for cc in held_cards]

    if request.to_add > 0:
        cc_response = await read_credit_cards_database(db=db, request=CreditCardsDatabaseRequest(card_details="all", use_preferences=True), current_user=user)
        ccs_added = [CreditCardSchema.model_validate(cc) for cc in cc_response.credit_card if cc not in ccs_used]

    W, categories, card_names_used, reward_relations_used = create_cards_matrix(ccs_used, heavy_hitters=heavy_hitters_response)
    ADD, _, card_names_added, reward_relations_added = create_cards_matrix(ccs_added, heavy_hitters=heavy_hitters_response)
    wallet_size = W.shape[1]

    W = np.hstack([W, ADD])

    card_names = card_names_used + card_names_added
    reward_relations = {**reward_relations_used, **reward_relations_added}

    # Calculate reward matrix R
    H_vector, categories = create_heavy_hitter_vector(heavy_hitters=heavy_hitters_response)
    R = W.T * H_vector  # Element-wise multiplication
    M = abs(sum(H_vector)) * 10

    card_sob_data = {}  # Key: card index i, Value: dict with SOB details

    # Annual fees
    C, H = R.shape

    for idx in range(C):
        card = None
        if idx >= wallet_size:
            card = ccs_added[idx - wallet_size]
        elif request.wallet_override and idx in is_new_flags:
            print("[INFO] Considering sign on bonus for a held card")
            card = ccs_used[idx]
        
        if card and card.sign_on_bonus and request.use_sign_on_bonus:
            for sob in card.sign_on_bonus:
                category = sob.purchase_type
                
                if category == PurchaseCategory.UNKNOWN:
                    continue  # Skip unknown categories

                threshold = sob.condition_amount
                T = sob.get_timeframe_in_months()
                sob_amount = sob.reward_amount * RewardUnit.get_value(sob.reward_type)
                max_level = int(threshold + 1000)
                levels = [l for l in range(500, max_level + 1, 500)]
                levels = sorted(set(levels))  # Ensure unique, sorted levels
                # Compute incremental probabilities
                levels_and_probs = await calculate_incremental_spending_probabilities(
                    user=user,
                    db=db,
                    category=category,
                    levels=levels,
                    T=T
                )
                incremental_probs = {}
                for l, p in levels_and_probs:
                    incremental_probs[l] = p

                # Store the data
                card_sob_data[idx] = {
                    'category': category,
                    'levels': levels,
                    'reward_unit' : sob.reward_type,
                    'incremental_probs': deepcopy(incremental_probs),
                    'sob_amount': sob_amount,
                    'timeframe': T
                }

    annual_fee_values = [0.0] * C
    for idx in range(C):
        if idx >= wallet_size:
            card = ccs_added[idx - wallet_size]
        else:
            card = ccs_used[idx]

        # Compute annual fees (annual fees are always in USD)
        if card.annual_fee:
            waived_years = card.annual_fee.waived_for
            effective_years = max(0, calculate_timeframe_years(timeframe=heavy_hitters_response.timeframe) - waived_years)
            annual_fee = effective_years * card.annual_fee.fee_usd
            annual_fee_values[idx] = annual_fee
        else:
            annual_fee_values[idx] = 0.0

    annual_statement_credits = [0.0] * C
    for idx in range(C):
        if idx >= wallet_size:
            card = ccs_added[idx - wallet_size]
        else:
            card = ccs_used[idx]

        total_credit = 0.0
        # Compute annual statement credits
        if card.statement_credit:
            for statement_credit in card.statement_credit:
                if statement_credit.timeframe_months > 0:
                    periods_per_year = 12 / statement_credit.timeframe_months
                    credit_per_period = statement_credit.credit_amount * statement_credit.max_uses * RewardUnit.get_value(statement_credit.unit)
                    annual_credit = periods_per_year * credit_per_period
                    total_credit += annual_credit
        
        annual_statement_credits[idx] = total_credit

    return RMatrixDetails(
        R=R,
        wallet_size=wallet_size,
        to_add = request.to_add,
        ccs_added=ccs_added,
        to_use = request.to_use,
        ccs_used=ccs_used,
        annual_fees=annual_fee_values,
        annual_statement_credits=annual_statement_credits,
        timeframe=heavy_hitters_response.timeframe,
        categories=categories,
        card_names=card_names,
        reward_relations=reward_relations,
        heavy_hitter_vector=H_vector,
        card_sob_data=card_sob_data,
        M = M
    )