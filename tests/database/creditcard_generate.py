from creditcard.enums import * 
from creditcard.schemas import CreditCardSchema
from creditcard.utils.parse import RewardCategoryRelation, RewardAmount
from database.creditcard.creditcard import CreditCard
from database.creditcard.crud import create_credit_card
from typing import List

GENERIC_CHASE_CARD_NAME = "Generic Chase Card"
chase_reward_category_map : List[RewardCategoryRelation] = [RewardCategoryRelation(category=PurchaseCategory.DINING,
                                                                                   reward=RewardAmount(reward_unit=RewardUnit.CHASE_ULTIMATE_REWARDS, amount=2)),
                            RewardCategoryRelation(category=PurchaseCategory.TRAVEL,
                                                   reward=RewardAmount(reward_unit=RewardUnit.CHASE_ULTIMATE_REWARDS, amount=3)),
                            RewardCategoryRelation(category=PurchaseCategory.OTHER,
                                                   reward=RewardAmount(reward_unit=RewardUnit.CHASE_ULTIMATE_REWARDS, amount=1))]
chase_card = CreditCardSchema(
        name = GENERIC_CHASE_CARD_NAME,
        issuer = Issuer.CHASE,
        reward_category_map = chase_reward_category_map,
        benefits=[Benefit.AIRPORT_LOUNGE_ACCESS, Benefit.CONCIERGE_SERVICE],
        credit_needed=[CreditNeeded.EXCELLENT],
        apr=0.27
    ).credit_card()


GENERIC_AMEX_CARD_NAME = "Generic Amex Card"
amex_card = CreditCardSchema(
        name=GENERIC_AMEX_CARD_NAME,
        issuer=Issuer.AMERICAN_EXPRESS,
        reward_category_map=[
            RewardCategoryRelation(category=PurchaseCategory.DINING, reward=RewardAmount(reward_unit=RewardUnit.AMEX_MEMBERSHIP_REWARDS, amount=4)),
            RewardCategoryRelation(category=PurchaseCategory.GROCERIES, reward=RewardAmount(reward_unit=RewardUnit.AMEX_MEMBERSHIP_REWARDS, amount=3)),
            RewardCategoryRelation(category=PurchaseCategory.TRAVEL, reward=RewardAmount(reward_unit=RewardUnit.AMEX_MEMBERSHIP_REWARDS, amount=2))
        ],
        benefits=[Benefit.EXTENDED_WARRANTY, Benefit.PURCHASE_PROTECTION],
        credit_needed=[CreditNeeded.EXCELLENT],
        apr=0.25
    ).credit_card()

GENERIC_CITI_CARD_NAME = "Generic Citi Card"
citi_card : CreditCard = CreditCardSchema(
        name=GENERIC_CITI_CARD_NAME,
        issuer=Issuer.CITI,
        reward_category_map=[
            RewardCategoryRelation(category=PurchaseCategory.TRAVEL, reward=RewardAmount(reward_unit=RewardUnit.CITI_THANKYOU_POINTS, amount=3)),
            RewardCategoryRelation(category=PurchaseCategory.DINING, reward=RewardAmount(reward_unit=RewardUnit.CITI_THANKYOU_POINTS, amount=2)),
            RewardCategoryRelation(category=PurchaseCategory.OTHER, reward=RewardAmount(reward_unit=RewardUnit.CITI_THANKYOU_POINTS, amount=1))
        ],
        benefits=[Benefit.PRICE_PROTECTION, Benefit.PURCHASE_PROTECTION],
        credit_needed=[CreditNeeded.GOOD],
        apr=0.23
    ).credit_card()

all_cards = [chase_card, amex_card, citi_card]

def populate_all(db):
    out = []
    for card in all_cards:
        created_card = create_credit_card(db, card)
        out.append(created_card)
    return out
    