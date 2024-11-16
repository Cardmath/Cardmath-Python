from copy import deepcopy  
from creditcard.schemas import RewardCategoryRelation
from insights.optimal_cards.r_matrix import RMatrixDetails
from insights.schemas import OptimalCardsAllocationSolution, CardsUseSummary, SpendingPlanItem, OptimalCardsAllocationRequest

import creditcard.enums as enums
import logging 

def extract_solution(model, request: OptimalCardsAllocationRequest, rmatrix: RMatrixDetails, x, z, s_il, credit_reduction) -> OptimalCardsAllocationSolution:
    # Define a default RewardCategoryRelation with valid enum values
    default_reward_relation = RewardCategoryRelation(
        category=enums.PurchaseCategory.UNKNOWN.value,
        reward_unit=enums.RewardUnit.UNKNOWN.value,
        reward_amount=0.0
    )

    C, H = rmatrix.R.shape
    wallet_indices = list(range(rmatrix.wallet_size))
    eligible_indices = list(range(rmatrix.wallet_size, rmatrix.wallet_size + len(rmatrix.ccs_added)))
    total_reward_usd = round(model.getObjVal(), 2)

    # Extract results if feasible
    selected_cards = []
    for i in range(C):
        z_val = model.getVal(z[i])
        if z_val > 0.5:
            selected_cards.append(i)
            print(f"[INFO] Selected card {i}, z value: {z_val:.3f}")

    cards_added = []
    if request.return_cards_added:
        cards_added = [
            rmatrix.ccs_added[idx - rmatrix.wallet_size]
            for idx in selected_cards
            if idx in eligible_indices
        ]
        print(f"[INFO] {len(cards_added)} cards added of {len(eligible_indices)} eligible")

    cards_used = []
    if request.return_cards_used:
        cards_used = [
            rmatrix.ccs_used[idx]
            for idx in selected_cards
            if ((idx in wallet_indices) or request.use_all_wallet_cards)
        ]

    # Prepare summary and spending plan
    summary = []
    spending_plan = []
    total_regular_rewards_usd = 0.0
    total_sign_on_bonus_usd = 0.0
    total_annual_fees_usd = 0.0
    total_statement_credits_usd = 0.0

    # If the user wants to return all the used cards, then add them to the selected cards
    selected_cards_set = set(selected_cards)
    if request.use_all_wallet_cards:
        selected_cards_set = selected_cards_set.union(wallet_indices)
    
    for idx in selected_cards_set:
        card_name = rmatrix.card_names[idx]
        annual_fee = rmatrix.annual_fees[idx]
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

            # Extract the actual credit reduction applied
            credit_reduction_value = model.getVal(credit_reduction[(idx, j)])
            logging.debug(f"Credit reduction for {card_name} {category}: {credit_reduction_value}")
            total_statement_credits_usd += credit_reduction_value

            # Add to spending plan if spending is allocated
            if x_value > 0 or credit_reduction_value > 0:
                spending_plan.append(
                    SpendingPlanItem(
                        card_name=card_name,
                        category=category,
                        amount_value=reward,
                        reward_unit_amount=x_value * reward_amount,
                        reward_unit=reward_unit,
                        statement_credit_value=credit_reduction_value
                    )
                )

        # Sign-on bonus calculation
        total_sob_likelihood = 0.0
        sob_amount = 0.0
        sob_reward_unit = enums.RewardUnit.UNKNOWN
        if idx in rmatrix.card_sob_data:
            sob_info = rmatrix.card_sob_data[idx]
            levels = sob_info['levels']
            incremental_probs = deepcopy(sob_info['incremental_probs'])
            sob_amount = sob_info['sob_amount']
            sob_reward_unit = sob_info['reward_unit']
            for l in levels:
                s_value = model.getVal(s_il[idx][l])
                if s_value > 0.5:
                    print(f"Sign on bonus level {l}, prob {incremental_probs[l]} activated {sob_amount}")
                    est_sign_on_bonus += sob_amount * incremental_probs[l]
                    total_sob_likelihood += incremental_probs[l]

            total_sign_on_bonus_usd += est_sign_on_bonus
        total_regular_rewards_usd += total_rewards
        net_rewards = total_rewards + est_sign_on_bonus + total_statement_credits_usd - annual_fee
        summary.append(
            CardsUseSummary(
                name=card_name,
                profit_usd=total_rewards + est_sign_on_bonus + total_statement_credits_usd - annual_fee,
                annual_fee_usd=annual_fee,

                sign_on_bonus_reward_unit=sob_reward_unit,
                sign_on_bonus_estimated=est_sign_on_bonus,
                sign_on_bonus_likelihood=total_sob_likelihood,
                sign_on_bonus_total=sob_amount,

                regular_rewards_usd=total_regular_rewards_usd,
                net_rewards_usd=net_rewards,
                statement_credits_usd=total_statement_credits_usd
            )
        )

    net_rewards_usd = total_regular_rewards_usd + total_sign_on_bonus_usd + total_statement_credits_usd - total_annual_fees_usd

    return OptimalCardsAllocationSolution(
        timeframe=rmatrix.timeframe,
        total_reward_usd=total_reward_usd,
        total_regular_rewards_usd=round(total_regular_rewards_usd, 2),
        total_sign_on_bonus_usd=round(total_sign_on_bonus_usd, 2),
        total_statement_credits_usd=round(total_statement_credits_usd, 2),
        total_annual_fees_usd=round(total_annual_fees_usd, 2),
        net_rewards_usd=round(net_rewards_usd, 2),
        total_reward_allocation=selected_cards,
        summary=summary,
        spending_plan=spending_plan,
        cards_used=cards_used,
        cards_added=cards_added
    )