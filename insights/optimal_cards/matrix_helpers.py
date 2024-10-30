from creditcard.schemas import CreditCardSchema, RewardCategoryRelation
from insights.heavyhitters import HeavyHittersResponse, HeavyHitterSchema
from insights.utils import remove_duplicates_ordered
from typing import List, Tuple, Dict

import creditcard.enums as enums
import numpy as np

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
