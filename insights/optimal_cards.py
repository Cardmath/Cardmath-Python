from creditcard.endpoints.read_database import read_credit_cards_database, CreditCardsDatabaseRequest
from creditcard.enums import * 
from creditcard.schemas import CreditCardSchema
from database.auth.user import User
from insights.category_spending_prediction import compute_user_card_sign_on_bonus_value
from insights.heavyhitters import read_heavy_hitters, HeavyHittersRequest, HeavyHittersResponse, HeavyHitterSchema
from insights.schemas import MonthlyTimeframe
from pydantic import BaseModel, ConfigDict
from pyscipopt import Model, quicksum
from sqlalchemy.orm import Session
from typing import Optional, List

import creditcard.enums as enums
import numpy as np

class OptimalCardsAllocationRequest(BaseModel):
    to_use: Optional[int] = 4
    to_add: Optional[int] = 0
    timeframe: Optional[MonthlyTimeframe] = None
    use_sign_on_bonus: bool = False
    return_cards_used: Optional[bool] = False
    return_cards_added: Optional[bool] = False

class HeldCardsUseSummary(BaseModel):
    name: str
    value: float

class OptimalCardsAllocationResponse(BaseModel):
    timeframe: MonthlyTimeframe
    total_reward_usd: float
    total_reward_allocation: List[int]

    total_annual_fee_held_cards_usd: float = 0
    total_annual_fee_added_cards_usd: float = 0

    summary: Optional[List[HeldCardsUseSummary]] = None
    cards_used: Optional[List[CreditCardSchema]] = None
    cards_added: Optional[List[CreditCardSchema]] = None

def remove_duplicates_ordered(lst):
    seen = set()
    return [x for x in lst if x not in seen and not seen.add(x)]



def create_cards_matrix(cards : List[CreditCardSchema], heavy_hitters: HeavyHittersResponse) -> np.array:
    hh_list: List[HeavyHitterSchema] = heavy_hitters.heavyhitters   
    vendors = list(filter(lambda x: x is not None, [hh.name if hh.name else None for hh in hh_list]))
    categories: list = remove_duplicates_ordered([hh.category for hh in hh_list])

    cards_matrix = np.zeros((len(hh_list), len(cards)))
    # TODO this is super inefficient but i am lazy rn
    for j, card in enumerate(cards):
        for i, hh in enumerate(hh_list):
            hc_idx = categories.index(hh.category)
            # Find the index for the category in reward_category_map
            cc_idx = None
            if hh.category in [rcr.category for rcr in card.reward_category_map]:
                cc_idx = [rcr.category for rcr in card.reward_category_map].index(hh.category)
            elif enums.PurchaseCategory.GENERAL.value in [rcr.category for rcr in card.reward_category_map]:
                cc_idx = [rcr.category for rcr in card.reward_category_map].index(enums.PurchaseCategory.GENERAL.value)
            elif enums.PurchaseCategory.UNKNOWN.value in [rcr.category for rcr in card.reward_category_map]:
                cc_idx = [rcr.category for rcr in card.reward_category_map].index(enums.PurchaseCategory.UNKNOWN.value)
                print(f"[OpenAI Prompt WARNING] Used unknown category {hh.category} in {card.reward_category_map}")
            else:
                print(f"Could not find category {hh.category} in {card.reward_category_map}")

            # If a category index is found, calculate the reward
            if cc_idx is not None:
                reward_data = card.reward_category_map[cc_idx]
                r_unit_val = RewardUnit.get_value(reward_data.reward_unit)
                r_reward_amount = reward_data.reward_amount
                cards_matrix[hc_idx][j] = r_unit_val * r_reward_amount

            for reward_category_relation in card.reward_category_map:
                
                # Add the vendors to the matrix
                if hh.name == reward_category_relation.category.value:
                    cards_matrix[i][j] = RewardUnit.get_value(reward_category_relation.reward_unit) * reward_category_relation.reward_amount

                # Add the categories to the matrix
                elif hh.category == reward_category_relation.category.value:
                    cards_matrix[i][j] = RewardUnit.get_value(reward_category_relation.reward_unit) * reward_category_relation.reward_amount

    return cards_matrix

def create_wallet_matrix(user: User, heavy_hitters: HeavyHittersResponse) -> np.array:
    held_cards = user.credit_cards
    held_cards = [CreditCardSchema.model_validate(cc) for cc in held_cards] 
    return create_cards_matrix(held_cards, heavy_hitters)

def create_heavy_hitter_matrix(heavy_hitters: HeavyHittersResponse) -> np.array:
    hh_list: List[HeavyHitterSchema] = heavy_hitters.heavyhitters   
    vendors: list = remove_duplicates_ordered(([hh.name for hh in hh_list]))
    categories: list = remove_duplicates_ordered([hh.category for hh in hh_list])

    heavy_hitter_matrix = np.zeros((len(hh_list),len(hh_list)))
    categories_index = len(vendors)
    vendors_index = 0
    for hh in hh_list:
        if hh.name in vendors:
            heavy_hitter_matrix[vendors_index][vendors_index] = hh.amount
            vendors_index += 1
        elif hh.category in categories:
            heavy_hitter_matrix[categories_index][categories_index] = hh.amount
            categories_index += 1

    return heavy_hitter_matrix

class RMatrixDetails(BaseModel):
    R: np.array 
    wallet_size: int
    add_size: int
    ccs_added: List[CreditCardSchema]
    ccs_used: List[CreditCardSchema]
    timeframe: MonthlyTimeframe

    model_config = ConfigDict(arbitrary_types_allowed=True)

def calculate_timeframe_years(timeframe: MonthlyTimeframe) -> int:
    start_date = timeframe.start_month
    end_date = timeframe.end_month
    return max(1, (end_date.year - start_date.year + 1))

async def compute_r_matrix(db: Session, user: User, request: OptimalCardsAllocationRequest) -> RMatrixDetails:
    heavy_hitters_response: HeavyHittersResponse = await read_heavy_hitters(
        db=db, user=user, request=HeavyHittersRequest(account_ids="all", timeframe=request.timeframe)
    )
    
    # Process held (wallet) cards
    held_cards = user.credit_cards
    ccs_used = [CreditCardSchema.model_validate(cc) for cc in held_cards]
    W: np.array = create_cards_matrix(ccs_used, heavy_hitters=heavy_hitters_response)
    wallet_size = W.shape[1]

    # Initialize additional cards if needed
    add_size = 0
    ccs_added = []
    if request.to_add > 0:
        cc_response = await read_credit_cards_database(db=db, request=CreditCardsDatabaseRequest(card_details="all"))
        ccs_added = [CreditCardSchema.model_validate(cc) for cc in cc_response.credit_card if cc not in ccs_used]
    
        ADD: np.array = create_cards_matrix(ccs_added, heavy_hitters=heavy_hitters_response)
        add_size = ADD.shape[1]
        W = np.hstack([W, ADD])

    # Calculate reward matrix R
    H: np.array = create_heavy_hitter_matrix(heavy_hitters=heavy_hitters_response)
    R = W.T @ H

    # Return both held and added cards in RMatrixDetails
    return RMatrixDetails(R=R, wallet_size=wallet_size, add_size=add_size, ccs_added=ccs_added, ccs_used=ccs_used, timeframe=heavy_hitters_response.timeframe) 

async def optimize_credit_card_selection_milp(db: Session, user: User, request: OptimalCardsAllocationRequest) -> OptimalCardsAllocationResponse:
    rmatrix: RMatrixDetails = await compute_r_matrix(db=db, user=user, request=request)

    R = rmatrix.R
    wallet_size = rmatrix.wallet_size
    add_size = rmatrix.add_size
    timeframe_years = calculate_timeframe_years(rmatrix.timeframe)

    print(f"[INFO] Wallet size: {wallet_size}, add size: {add_size}")

    wallet_indices: List[int] = np.arange(0, wallet_size)
    eligible_indices: List[int] = np.arange(wallet_size, add_size + wallet_size)
    assert len(wallet_indices) + len(eligible_indices) == R.shape[0]
    
    model = Model("credit_card_selection")

    if R.shape[0] == 0:
        print("[ERROR] R matrix is empty")
        return OptimalCardsAllocationResponse(total_reward_usd=0, total_reward_allocation=[], summary=[], cards_used=[], cards_added=[])

    C = len(R)  # Number of cards
    H = len(R[0])  # Number of categories (columns)

    # Define binary variables for card-category assignment
    y = {(i, j): model.addVar(vtype="B", name=f"y[{i},{j}]") for i in range(C) for j in range(H)}

    # Calculate sign-on bonus and annual fee for each card
    sign_on_bonus_values = [0] * C
    if request.use_sign_on_bonus:
        for idx in range(C):
            card = rmatrix.ccs_added[idx - wallet_size] if idx >= wallet_size else rmatrix.ccs_used[idx]
            sign_on_bonus_values[idx] = await compute_user_card_sign_on_bonus_value(user, db, card)

    annual_fee_values = [0] * C
    for idx in range(C):
        card = rmatrix.ccs_added[idx - wallet_size] if idx >= wallet_size else rmatrix.ccs_used[idx]
        if card.annual_fee:
            waived_years = card.annual_fee.waived_for
            effective_years = max(0, timeframe_years - waived_years)
            annual_fee_values[idx] = effective_years * card.annual_fee.fee_usd

    # Objective function to maximize rewards, considering sign-on bonus and annual fee
    model.setObjective(
        quicksum(y[i, j] * (R[i][j] + sign_on_bonus_values[i] - annual_fee_values[i]) for i in range(C) for j in range(H)),
        "maximize"
    )

    # Constraint: Ensure only one card is assigned per category
    for j in range(H):
        model.addCons(quicksum(y[i, j] for i in range(C)) <= 1)

    # Constraints for total cards used based on request
    if request.to_use > wallet_size:
        request.to_use = wallet_size
    model.addCons(quicksum(y[i, j] for i in wallet_indices for j in range(H)) <= request.to_use)
    model.addCons(quicksum(y[i, j] for i in eligible_indices for j in range(H)) <= request.to_add)

    # Solve the model
    model.optimize()

    # Check feasibility
    if model.getStatus() != "optimal" and model.getStatus() != "feasible":
        print("[ERROR] No feasible solution found.")
        return OptimalCardsAllocationResponse(total_reward_usd=0, total_reward_allocation=[], summary=[], cards_used=[], cards_added=[])

    # Extract results if feasible
    selected_cards = [i for i in range(C) if any(model.getVal(y[i, j]) > 0.5 for j in range(H))]
    total_reward_usd = round(model.getObjVal(), 2)

    cards_added = []
    if request.return_cards_added:
        cards_added = [card for idx, card in enumerate(rmatrix.ccs_added) if idx + wallet_size in eligible_indices and idx + wallet_size in selected_cards]
        print(f"[INFO] {len(cards_added)} cards added of {len(eligible_indices)} eligible")

    cards_used = []
    if request.return_cards_used:
        cards_used = [CreditCardSchema.model_validate(cc) for cc in rmatrix.ccs_used]

    return OptimalCardsAllocationResponse(
        timeframe=rmatrix.timeframe,
        total_reward_usd=total_reward_usd,
        total_reward_allocation=selected_cards,
        summary=None,
        cards_used=cards_used,
        cards_added=cards_added
    )