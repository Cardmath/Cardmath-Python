from collections import defaultdict
from copy import deepcopy
from creditcard.endpoints.read_database import read_credit_cards_database, CreditCardsDatabaseRequest
from creditcard.schemas import CreditCardSchema, RewardCategoryRelation, RewardCategoryThreshold
from database.auth.user import User
from insights.category_spending_prediction import calculate_incremental_spending_probabilities
from insights.heavyhitters import read_heavy_hitters, HeavyHittersRequest, HeavyHittersResponse, HeavyHitterSchema
from insights.schemas import MonthlyTimeframe
from pydantic import BaseModel, ConfigDict
from pyscipopt import Model, quicksum
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Tuple

import creditcard.enums as enums
import numpy as np
import datetime

class OptimalCardsAllocationRequest(BaseModel):
    to_use: Optional[int] = 4
    to_add: Optional[int] = 0
    timeframe: Optional[MonthlyTimeframe] = None
    use_sign_on_bonus: bool = False
    return_cards_used: Optional[bool] = False
    return_cards_added: Optional[bool] = False

class CardsUseSummary(BaseModel):
    name: str 

    annual_fee_usd: float
    sign_on_bonus_estimated: float
    sign_on_bonus_likelihood: float
    sign_on_bonus_reward_unit: enums.RewardUnit
    sign_on_bonus_total: float
    regular_rewards_usd: float

    profit_usd: float
    
class SpendingPlanItem(BaseModel):
    card_name: str
    category: str
    amount_value: float
    reward_unit_amount: float
    reward_unit: str

class OptimalCardsAllocationResponse(BaseModel):
    timeframe: MonthlyTimeframe
    total_reward_usd: float
    total_regular_rewards_usd: float
    total_sign_on_bonus_usd: float
    total_annual_fees_usd: float
    net_rewards_usd: float

    total_reward_allocation: List[int]
    summary: Optional[List[CardsUseSummary]] = None
    spending_plan: Optional[List[SpendingPlanItem]] = None
    actionable_steps: Optional[List[str]] = None

    cards_used: Optional[List[CreditCardSchema]] = None
    cards_added: Optional[List[CreditCardSchema]] = None

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

def create_cards_matrix(cards: List[CreditCardSchema], heavy_hitters: HeavyHittersResponse) -> Tuple[np.array, List[str], List[str], Dict[Tuple[str, str], RewardCategoryRelation]]:
    hh_list: List[HeavyHitterSchema] = heavy_hitters.heavyhitters
    vendors = list(filter(lambda x: x is not None, [hh.name if hh.name else None for hh in hh_list]))
    categories: list = remove_duplicates_ordered([hh.category for hh in hh_list])

    num_categories = len(categories)
    num_cards = len(cards)
    cards_matrix = np.zeros((num_categories, num_cards))
    reward_relations = {}

    for j, card in enumerate(cards):
        for i, category in enumerate(categories):
            # Find the best reward for this category
            best_reward = None
            for reward_relation in card.reward_category_map:
                if reward_relation.category == category or reward_relation.category == enums.PurchaseCategory.GENERAL.value:
                    best_reward = reward_relation
                    break  # Assume the first match is the best (adjust if needed)

            if best_reward:
                reward_relations[(card.name, category)] = best_reward
                r_unit_val = enums.RewardUnit.get_value(best_reward.reward_unit)
                r_reward_amount = best_reward.reward_amount
                cards_matrix[i][j] = r_unit_val * r_reward_amount
            else:
                # No reward for this category
                cards_matrix[i][j] = 0

    return cards_matrix, categories, [card.name for card in cards], reward_relations

def create_heavy_hitter_vector(heavy_hitters: HeavyHittersResponse) -> Tuple[np.array, List[str]]:
    hh_list: List[HeavyHitterSchema] = heavy_hitters.heavyhitters
    categories: list = remove_duplicates_ordered([hh.category for hh in hh_list])

    num_categories = len(categories)
    heavy_hitter_vector = np.zeros(num_categories)
    for i, category in enumerate(categories):
        total_amount = sum(hh.amount for hh in hh_list if hh.category == category)
        heavy_hitter_vector[i] = total_amount

    return heavy_hitter_vector, categories

class RMatrixDetails(BaseModel):
    R: np.array
    wallet_size: int
    add_size: int
    ccs_added: List[CreditCardSchema]
    ccs_used: List[CreditCardSchema]
    timeframe: MonthlyTimeframe
    categories: List[str]
    card_names: List[str]
    reward_relations: Dict[Tuple[str, str], RewardCategoryRelation]
    heavy_hitter_vector: np.array

    model_config = ConfigDict(arbitrary_types_allowed=True)

async def compute_r_matrix(db: Session, user: User, request: OptimalCardsAllocationRequest) -> RMatrixDetails:
    heavy_hitters_response: HeavyHittersResponse = await read_heavy_hitters(
        db=db, user=user, request=HeavyHittersRequest(account_ids="all", timeframe=request.timeframe)
    )

    # Process held (wallet) cards
    held_cards = user.credit_cards
    ccs_used = [CreditCardSchema.model_validate(cc) for cc in held_cards]
    W, categories, card_names_used, reward_relations_used = create_cards_matrix(ccs_used, heavy_hitters=heavy_hitters_response)
    wallet_size = W.shape[1]

    # Initialize additional cards if needed
    add_size = 0
    ccs_added = []
    reward_relations_added = {}
    if request.to_add > 0:
        cc_response = await read_credit_cards_database(db=db, request=CreditCardsDatabaseRequest(card_details="all", use_preferences=True), current_user=user)
        ccs_added = [CreditCardSchema.model_validate(cc) for cc in cc_response.credit_card if cc not in ccs_used]

        ADD, _, card_names_added, reward_relations_added = create_cards_matrix(ccs_added, heavy_hitters=heavy_hitters_response)
        add_size = ADD.shape[1]
        W = np.hstack([W, ADD])
        card_names = card_names_used + card_names_added
        reward_relations = {**reward_relations_used, **reward_relations_added}
    else:
        card_names = card_names_used
        reward_relations = reward_relations_used

    # Calculate reward matrix R
    H_vector, categories = create_heavy_hitter_vector(heavy_hitters=heavy_hitters_response)
    R = W.T * H_vector  # Element-wise multiplication

    return RMatrixDetails(
        R=R,
        wallet_size=wallet_size,
        add_size=add_size,
        ccs_added=ccs_added,
        ccs_used=ccs_used,
        timeframe=heavy_hitters_response.timeframe,
        categories=categories,
        card_names=card_names,
        reward_relations=reward_relations,
        heavy_hitter_vector=H_vector
    )

async def optimize_credit_card_selection_milp(
    db: Session,
    user: User,
    request: OptimalCardsAllocationRequest
) -> OptimalCardsAllocationResponse:
    rmatrix: RMatrixDetails = await compute_r_matrix(db=db, user=user, request=request)

    R = rmatrix.R
    wallet_size = rmatrix.wallet_size
    add_size = rmatrix.add_size
    timeframe_months = calculate_timeframe_months(rmatrix.timeframe)
    timeframe_years = max(1, timeframe_months // 12)

    print(f"[INFO] Wallet size: {wallet_size}, add size: {add_size}")

    wallet_indices: List[int] = np.arange(0, wallet_size)
    eligible_indices: List[int] = np.arange(wallet_size, add_size + wallet_size)
    assert len(wallet_indices) + len(eligible_indices) == R.shape[0]

    model = Model("credit_card_selection")

    if R.shape[0] == 0:
        print("[ERROR] R matrix is empty")
        return OptimalCardsAllocationResponse(
            timeframe=rmatrix.timeframe,
            total_reward_usd=0,
            total_regular_rewards_usd=0,
            total_sign_on_bonus_usd=0,
            total_annual_fees_usd=0,
            net_rewards_usd=0,
            total_reward_allocation=[],
            summary=[],
            cards_used=[],
            cards_added=[]
        )

    C = R.shape[0]  # Number of cards
    H = R.shape[1]  # Number of categories

    # Decision variables: amount of spending in category assigned to a card
    x = {}
    for i in range(C):
        for j in range(H):
            x[(i, j)] = model.addVar(vtype="C", lb=0.0, name=f"x[{i},{j}]")

    # Constraint: Total spending in each category cannot exceed projected spending
    for j in range(H):
        model.addCons(
            quicksum(x[(i, j)] for i in range(C)) <= rmatrix.heavy_hitter_vector[j],
            name=f"TotalSpending_Category_{j}"
        )

    # Objective function components
    objective_terms = []

    # Auxiliary variables for thresholds
    y_vars = {}

    # Define a default RewardCategoryRelation with valid enum values
    default_reward_relation = RewardCategoryRelation(
        category=enums.PurchaseCategory.UNKNOWN.value,
        reward_unit=enums.RewardUnit.UNKNOWN.value,
        reward_amount=0.0
    )

    # Binary variables for card usage
    z = {i: model.addVar(vtype="B", name=f"z[{i}]") for i in range(C)}

    # Linking constraints between x and z
    M = abs(sum(rmatrix.heavy_hitter_vector)) * 10  # Big M value
    print(f"[INFO] Big M value: {M}")
    for i in range(C):
        for j in range(H):
            model.addCons(x[(i, j)] <= M * z[i], name=f"Linking_{i}_{j}")

    # Constraints for total cards used based on request
    if request.to_use > wallet_size:
        request.to_use = wallet_size
    model.addCons(quicksum(z[i] for i in wallet_indices) <= request.to_use, name="MaxHeldCards")
    model.addCons(quicksum(z[i] for i in eligible_indices) <= request.to_add, name="MaxAddedCards")

    # Collect sign-on bonus data
    card_sob_data = {}  # Key: card index i, Value: dict with SOB details

    for idx in range(C):
        if idx >= wallet_size:
            card = rmatrix.ccs_added[idx - wallet_size]
        else:
            continue  # We assume existing cards don't have new SOBs
        if request.use_sign_on_bonus:
            for sob in card.sign_on_bonus:
                category = sob.purchase_type
                
                if category == enums.PurchaseCategory.UNKNOWN:
                    break  # Skip unknown categories

                threshold = sob.condition_amount
                T = sob.get_timeframe_in_months()
                sob_amount = sob.reward_amount * enums.RewardUnit.get_value(sob.reward_type)
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

    # Create variables for sign-on bonuses
    s_il = {}  # Key: (i, l), Value: binary variable s_il
    
    for i, sob_info in card_sob_data.items():
        category = sob_info['category']
        levels = sob_info['levels']
        incremental_probs = sob_info['incremental_probs']
        sob_amount = sob_info['sob_amount']
        
        # Find the index j of the category in rmatrix.categories
        if category in rmatrix.categories:
            j = rmatrix.categories.index(category)
        else:
            # If category is not in user's spending, skip
            continue

        # Create binary variables s_il
        s_il[i] = {}
        levels = sorted(levels)
        for l in levels:
            s_il[i][l] = model.addVar(vtype="B", name=f"s_{i}_{l}")
        # Add spending level activation constraints
        for l in levels:
            if category == enums.PurchaseCategory.GENERAL:
                model.addCons(
                    quicksum(x[(i, j)] for j in range(H)) >= l * s_il[i][l],
                    name=f"SpendingLevelActivation_{i}_{l}"
                )
            else :
                model.addCons(
                    x[(i, j)] >= l * s_il[i][l],
                    name=f"SpendingLevelActivation_{i}_{l}"
                )
        # Add sequential activation constraints
        for idx_level in range(1, len(levels)):
            l_current = levels[idx_level]
            l_prev = levels[idx_level - 1]
            model.addCons(
                s_il[i][l_current] <= s_il[i][l_prev],
                name=f"SequentialActivation_{i}_{l_current}"
            )
        # Ensure s_il[i][l] <= z[i]
        for l in levels:
            model.addCons(
                s_il[i][l] <= z[i],
                name=f"SOBActivation_{i}_{l}"
            )
        # Add to objective function
        for l in levels:
            EV_il = sob_amount * incremental_probs[l]
            objective_terms.append(EV_il * s_il[i][l])

    # Add constraints and objective function terms for each card and category
    for i in range(C):
        card_name = rmatrix.card_names[i]
        for j in range(H):
            category = rmatrix.categories[j]
            card_category_key = (card_name, category)
            reward_relation = rmatrix.reward_relations.get(
                card_category_key, default_reward_relation
            )

            reward_amount = reward_relation.reward_amount
            reward_unit = reward_relation.reward_unit

            # Handle thresholds
            if reward_relation.reward_threshold:
                threshold_info = reward_relation.reward_threshold
                threshold = threshold_info.on_up_to_purchase_amount_usd
                per_timeframe_months = threshold_info.per_timeframe_num_months
                fallback_reward = threshold_info.fallback_reward_amount

                if threshold > 0 and per_timeframe_months > 0:
                    # Calculate how many times the threshold timeframe fits into the computation timeframe
                    num_threshold_periods = max(1, timeframe_months // per_timeframe_months)
                    effective_threshold = threshold * num_threshold_periods

                    # Variables for spending within and beyond the threshold
                    y1_var_name = f"y1_{i}_{j}"
                    y2_var_name = f"y2_{i}_{j}"
                    y1 = model.addVar(vtype="C", lb=0.0, name=y1_var_name)
                    y2 = model.addVar(vtype="C", lb=0.0, name=y2_var_name)

                    y_vars[(i, j)] = (y1, y2)

                    # Constraint: y1 ≤ effective_threshold
                    model.addCons(y1 <= effective_threshold, name=f"Threshold_{i}_{j}")

                    # Constraint: x = y1 + y2
                    model.addCons(
                        x[(i, j)] == y1 + y2,
                        name=f"Split_{i}_{j}"
                    )

                    # Add to objective function
                    reward_multiplier = enums.RewardUnit.get_value(reward_unit) * reward_amount
                    fallback_multiplier = enums.RewardUnit.get_value(reward_unit) * fallback_reward
                    objective_terms.append(reward_multiplier * y1)
                    objective_terms.append(fallback_multiplier * y2)
                else:
                    # No effective threshold; use x directly
                    reward_multiplier = enums.RewardUnit.get_value(reward_unit) * reward_amount
                    objective_terms.append(reward_multiplier * x[(i, j)])
            else:
                # No threshold; use x directly
                reward_multiplier = enums.RewardUnit.get_value(reward_unit) * reward_amount
                objective_terms.append(reward_multiplier * x[(i, j)])

    # Annual fees
    annual_fee_values = [0.0] * C
    for idx in range(C):
        if idx >= wallet_size:
            card = rmatrix.ccs_added[idx - wallet_size]
        else:
            card = rmatrix.ccs_used[idx]

        # Compute annual fees (annual fees are always in USD)
        if card.annual_fee:
            waived_years = card.annual_fee.waived_for
            effective_years = max(0, timeframe_years - waived_years)
            annual_fee = effective_years * card.annual_fee.fee_usd
            annual_fee_values[idx] = annual_fee
        else:
            annual_fee_values[idx] = 0.0

    # Add annual fees to the objective function
    objective_terms += [-annual_fee_values[i] * z[i] for i in range(C)]

    # Set the objective function
    model.setObjective(quicksum(objective_terms), "maximize")

    # use this to debug
    # if (request.use_sign_on_bonus):
    #     model.writeProblem("milp_debug.lp")

    # Solve the model
    model.optimize()

    # Check feasibility
    status = model.getStatus()
    if status not in ["optimal", "feasible"]:
        print("[ERROR] No feasible solution found.")
        return OptimalCardsAllocationResponse(
            timeframe=rmatrix.timeframe,
            total_reward_usd=0,
            total_regular_rewards_usd=0,
            total_sign_on_bonus_usd=0,
            total_annual_fees_usd=0,
            net_rewards_usd=0,
            total_reward_allocation=[],
            summary=[],
            cards_used=[],
            cards_added=[]
        )

    # Extract results if feasible
    selected_cards = []
    for i in range(C):
        z_val = model.getVal(z[i])
        if z_val > 0.5:
            selected_cards.append(i)
            print(f"[INFO] Selected card {i}, z value: {z_val:.3f}")
    total_reward_usd = round(model.getObjVal(), 2)

    cards_added = []
    if request.return_cards_added:
        cards_added = [
            rmatrix.ccs_added[idx - wallet_size]
            for idx in selected_cards
            if idx in eligible_indices
        ]
        print(f"[INFO] {len(cards_added)} cards added of {len(eligible_indices)} eligible")

    cards_used = []
    if request.return_cards_used:
        cards_used = [
            rmatrix.ccs_used[idx]
            for idx in selected_cards
            if idx in wallet_indices
        ]

    # Prepare summary and spending plan
    summary = []
    spending_plan = []
    total_regular_rewards_usd = 0.0
    total_sign_on_bonus_usd = 0.0
    total_annual_fees_usd = 0.0

    for idx in selected_cards:
        card_name = rmatrix.card_names[idx]
        annual_fee = annual_fee_values[idx]
        total_annual_fees_usd += annual_fee
        total_rewards = 0.0
        est_sign_on_bonus = 0.0
        # Regular rewards from spending
        for j in range(H):
            category = rmatrix.categories[j]
            reward_relation = rmatrix.reward_relations.get(
                (card_name, category),
                default_reward_relation
            )
            reward_amount = reward_relation.reward_amount
            reward_unit = reward_relation.reward_unit
            x_value = model.getVal(x[(idx, j)])
            # Adjust reward calculation based on reward unit
            reward_multiplier = enums.RewardUnit.get_value(reward_unit) * reward_amount
            reward = x_value * reward_multiplier
            total_rewards += reward

            # Add to spending plan if spending is allocated
            if x_value > 0:
                spending_plan.append(
                    SpendingPlanItem(
                        card_name=card_name,
                        category=category,
                        amount_value=reward,
                        reward_unit_amount=x_value * reward_amount,
                        reward_unit=reward_unit
                    )
                )
        # Sign-on bonus calculation
        total_sob_likelihood = 0.0
        sob_amount = 0.0
        sob_reward_unit = enums.RewardUnit.UNKNOWN
        if idx in card_sob_data:
            sob_info = card_sob_data[idx]
            levels = sob_info['levels']
            incremental_probs = deepcopy(sob_info['incremental_probs'])
            sob_amount = sob_info['sob_amount']
            sob_reward_unit = sob_info['reward_unit']
            for l in levels:
                s_value = model.getVal(s_il[idx][l])
                if s_value > 0.5:
                    print(f"Sign on bonus level {l}, prob {incremental_probs[l]} activated { sob_amount }")
                    est_sign_on_bonus += sob_amount * incremental_probs[l]
                    total_sob_likelihood += incremental_probs[l]
            
            total_sign_on_bonus_usd += est_sign_on_bonus
        total_regular_rewards_usd += total_rewards
        net_rewards = total_rewards + est_sign_on_bonus - annual_fee
        summary.append(
            CardsUseSummary(
                name=card_name,
                profit_usd=total_rewards + est_sign_on_bonus - annual_fee,
                annual_fee_usd=annual_fee,
                
                sign_on_bonus_reward_unit=sob_reward_unit,
                sign_on_bonus_estimated=est_sign_on_bonus,
                sign_on_bonus_likelihood=total_sob_likelihood,
                sign_on_bonus_total=sob_amount,

                regular_rewards_usd=total_regular_rewards_usd,
                net_rewards_usd=net_rewards
            )
        )

    net_rewards_usd = total_regular_rewards_usd + total_sign_on_bonus_usd - total_annual_fees_usd

    # Prepare actionable steps
    actionable_steps = []
    if cards_added:
        actionable_steps.append("Apply for the recommended credit cards.")
    if spending_plan:
        actionable_steps.append("Allocate your spending according to the spending plan.")
    # Add more steps as needed

    return OptimalCardsAllocationResponse(
        timeframe=rmatrix.timeframe,
        total_reward_usd=total_reward_usd,
        total_regular_rewards_usd=round(total_regular_rewards_usd, 2),
        total_sign_on_bonus_usd=round(total_sign_on_bonus_usd, 2),
        total_annual_fees_usd=round(total_annual_fees_usd, 2),
        net_rewards_usd=round(net_rewards_usd, 2),
        total_reward_allocation=selected_cards,
        summary=summary,
        spending_plan=spending_plan,
        actionable_steps=actionable_steps,
        cards_used=cards_used,
        cards_added=cards_added
    )
