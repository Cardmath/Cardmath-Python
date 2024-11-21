from creditcard.schemas import RewardCategoryRelation 
from insights.schemas import OptimalCardsAllocationRequest, RMatrixDetails
from insights.utils import calculate_timeframe_years, calculate_timeframe_months
from pyscipopt import Model, quicksum
from typing import Dict, Tuple

import creditcard.enums as enums
import logging
import numpy as np

def initialize_model(rmatrix: RMatrixDetails, credit_values: np.ndarray):
    model = Model("credit_card_selection")

    C, H = rmatrix.R.shape
    x = {(i, j): model.addVar(vtype="C", lb=0.0, name=f"x[{i},{j}]") for i in range(C) for j in range(H)}
    z = {i: model.addVar(vtype="B", name=f"z[{i}]") for i in range(C)}

    # Define auxiliary variables for statement credit reductions
    credit_reduction = {(i, j): model.addVar(vtype="C", lb=0.0, name=f"credit_reduction[{i},{j}]") for i in range(C) for j in range(H)}

    # Link auxiliary variables to statement credits
    for i in range(C):
        for j in range(H):
            model.addCons(
                credit_reduction[(i, j)] <= credit_values[i, j] * z[i],
                name=f"CreditReductionBound[{i},{j}]"
            )

    # Adjust spending constraints using auxiliary variables
    H_vector: np.array = rmatrix.heavy_hitter_vector
    for j in range(H):
        model.addCons(
            quicksum(x[(i, j)] for i in range(C)) - quicksum(credit_reduction[(i, j)] for i in range(C)) >= 0,
            name=f"NonNegativeSpending_Category_{j}"
        )
        model.addCons(
            quicksum(x[(i, j)] for i in range(C)) <= H_vector[j],
            name=f"TotalSpending_Category_{j}"
        )

    M = rmatrix.M
    for i in range(C):
        for j in range(H):
            model.addCons(x[(i, j)] <= M * z[i], name=f"Linking_{i}_{j}")

    # Add constraints for the maximum number of cards allowed to be used and added
    wallet_indices = list(range(rmatrix.wallet_size))
    eligible_indices = list(range(rmatrix.wallet_size, rmatrix.wallet_size + len(rmatrix.ccs_added)))
    
    model.addCons(quicksum(z[i] for i in wallet_indices + eligible_indices) <= rmatrix.to_use, name="MaxHeldCards")
    model.addCons(quicksum(z[i] for i in eligible_indices) <= rmatrix.to_add, name="MaxAddedCards")
        
    return model, x, z, credit_reduction

def add_linking_constraints(model: Model, rmatrix : RMatrixDetails, x: Dict[Tuple[int, int], Model], z: Dict[int, Model]):
    """Link spending variables (x) with binary usage variables (z) using a large constant M."""
    C, H = rmatrix.R.shape

def consider_reward_category(model: Model, x: Dict[Tuple[int, int], Model], rmatrix: RMatrixDetails):
    # Add constraints and objective function terms for each card and category
    objective_terms = []
    
    y_vars = {}

    default_reward_relation = RewardCategoryRelation(
        category=enums.PurchaseCategory.UNKNOWN.value,
        reward_unit=enums.RewardUnit.UNKNOWN.value,
        reward_amount=0.0
    )

    C, H = rmatrix.R.shape
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
                    num_threshold_periods = max(
                        1, 
                        calculate_timeframe_months(rmatrix.timeframe) // per_timeframe_months
                    )
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
                    if per_timeframe_months == 0:
                        logging.warning(
                            f"Per timeframe months is zero for card {card_name}, category {category}. "
                            "Skipping threshold handling to avoid division by zero."
                        )
                    # No effective threshold; use x directly
                    reward_multiplier = enums.RewardUnit.get_value(reward_unit) * reward_amount
                    objective_terms.append(reward_multiplier * x[(i, j)])
            else:
                # No threshold; use x directly
                reward_multiplier = enums.RewardUnit.get_value(reward_unit) * reward_amount
                objective_terms.append(reward_multiplier * x[(i, j)])

    return y_vars, objective_terms

def consider_annual_fee(model: Model, z: Dict[int, Model], rmatrix: RMatrixDetails):
    """Add annual fee terms to the model's objective."""
    objective_terms = []
    C = len(z)
    for i in range(C):
        annual_fee = calculate_timeframe_years(timeframe=rmatrix.timeframe) * rmatrix.ccs_used[i].annual_fee.fee_usd if i < rmatrix.wallet_size else rmatrix.ccs_added[i - rmatrix.wallet_size].annual_fee.fee_usd
        objective_terms.append(-annual_fee * z[i])
    return objective_terms

def precompute_credit_values(rmatrix: RMatrixDetails) -> np.ndarray:
    """
    Precompute the annualized statement credit values for each card-category pair.

    Args:
        rmatrix (RMatrixDetails): Contains the reward matrix and associated metadata.

    Returns:
        np.ndarray: A 2D array of annualized statement credit values for each card and category.
    """
    logging.info("Starting precomputation of annualized statement credit values.")
    
    C, H = rmatrix.R.shape
    credit_values = np.zeros((C, H))

    for i in range(C):
        card = None
        wallet_size = rmatrix.wallet_size
        if i >= wallet_size:
            card = rmatrix.ccs_added[i - wallet_size]
        else:
            card = rmatrix.ccs_used[i]
            
        for j in range(H):
            category = rmatrix.categories[j]
            statement_credits = card.statement_credit
            
            for sc in statement_credits:
                if not sc.categories or category in sc.categories:
                    if sc.timeframe_months != 0:
                        max_uses = min(
                            sc.max_uses,
                            calculate_timeframe_months(rmatrix.timeframe) / sc.timeframe_months
                        )
                        annualization_factor = calculate_timeframe_years(rmatrix.timeframe) * (12 / sc.timeframe_months)
                        credit_value = sc.credit_amount * max_uses * annualization_factor
                    else:
                        logging.warning(
                            f"Statement credit timeframe_months is zero for card {card.name}, category {category}. "
                            "Skipping this credit to avoid division by zero."
                        )
                        credit_value = 0.0

                    credit_values[i, j] += credit_value
                
            logging.debug(
                f"Card: {card.name}, Category: {category}, "
                f"Statement Credits Applied: {len(statement_credits)}, "
                f"Credit Value: {credit_values[i, j]}"
            )

    logging.info("Completed precomputation of statement credit values.")
    return credit_values

def consider_sign_on_bonus(model: Model, x: Dict[Tuple[int, int], Model], z: Dict[int, Model], rmatrix: RMatrixDetails):
    '''
    Outputs s_il dict
    '''
    objective_terms = []
    C, H = rmatrix.R.shape

    # Create variables for sign-on bonuses
    s_il = {}  # Key: (i, l), Value: binary variable s_il
    sob_data = rmatrix.card_sob_data
    for i, sob_info in sob_data.items():
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

    return s_il, objective_terms

def setup_model(request: OptimalCardsAllocationRequest, rmatrix: RMatrixDetails) -> Model:
    """Initialize the model, add decision variables, constraints, and objective terms."""
    # Precompute credit values for statement credits
    credit_values = precompute_credit_values(rmatrix=rmatrix)

    # Initialize model
    model, x, z, credit_reduction = initialize_model(rmatrix=rmatrix, credit_values=credit_values)

    # Add terms for rewards, annual fees, and statement credits
    y_vars, rc_terms = consider_reward_category(model=model, x=x, rmatrix=rmatrix)
    annual_fee_terms = consider_annual_fee(model=model, z=z, rmatrix=rmatrix)

    # Add statement credits directly to the objective
    statement_credit_terms = [
        credit_reduction[(i, j)]
        for i in range(rmatrix.R.shape[0])
        for j in range(rmatrix.R.shape[1])
    ]

    s_il, sob_terms = {}, []
    if request.use_sign_on_bonus:    
        s_il, sob_terms = consider_sign_on_bonus(model=model, x=x, z=z, rmatrix=rmatrix)
    
    # Set the objective function
    model.setObjective(quicksum(annual_fee_terms + sob_terms + rc_terms + statement_credit_terms), "maximize")
    
    return model, x, z, s_il, credit_reduction
