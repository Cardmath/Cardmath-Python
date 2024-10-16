from creditcard.endpoints.read_database import read_credit_cards_database, CreditCardsDatabaseRequest
from creditcard.enums import * 
from creditcard.schemas import CreditCardSchema
from database.auth.user import User
from database.creditcard.creditcard import CreditCard
from insights.heavyhitters import read_heavy_hitters, HeavyHittersRequest, HeavyHittersResponse, HeavyHitterSchema
from pydantic import BaseModel, model_validator
from sqlalchemy.orm import Session
from typing import Optional, List
import numpy as np

class OptimalCardsAllocationRequest(BaseModel):
    held_cards_only: bool = False
    all_cards: bool = False
    save_to_db: bool = False

    @model_validator(mode="before")
    @classmethod
    def not_all_cards_and_held_cards_only(cls, v):
        if v.get("all_cards") and v.get("held_cards_only"):
            raise ValueError("Cannot be all cards and held cards only")
        return v

class HeldCardsUseSummary(BaseModel):
    name: str
    value: float

class OptimalCardsAllocationResponse(BaseModel):
    total_reward_usd: float
    total_reward_allocation: List[int]
    summary: Optional[List[HeldCardsUseSummary]] = None

async def compute_optimal_cards_allocation(db: Session, user: User, request: OptimalCardsAllocationRequest) -> OptimalCardsAllocationResponse:
    heavy_hitters_response: HeavyHittersResponse = await read_heavy_hitters(db=db, user=user, request=HeavyHittersRequest(account_ids="all"))    
    W = None
    if request.held_cards_only:
        W: np.array = create_wallet_matrix(user=user, heavy_hitters=heavy_hitters_response)
    elif request.all_cards:
        cc_response = await read_credit_cards_database(db=db, request=CreditCardsDatabaseRequest(card_details="all"))
        W = create_cards_matrix(cc_response.credit_card, heavy_hitters=heavy_hitters_response)
    H: np.array = create_heavy_hitter_matrix(heavy_hitters=heavy_hitters_response)
    R = W.T @ H
    r = round(float(np.sum(np.max(R, axis=1))), 2)
    r_idx = list(np.argmax(R, axis=1))

    print(R)

    return OptimalCardsAllocationResponse(total_reward_usd=r, total_reward_allocation=r_idx, summary=None)

def create_cards_matrix(cards : List[CreditCardSchema], heavy_hitters: HeavyHittersResponse) -> np.array:
    categories: List[HeavyHitterSchema] = heavy_hitters.categories    
    vendors: List[HeavyHitterSchema] = heavy_hitters.vendors

    cards_matrix = np.zeros((len(categories), len(cards)))
    # TODO this is super inefficient but i am lazy rn
    for j, card in enumerate(cards):
        for i, category in enumerate(categories):
            for reward_category_relation in card.reward_category_map:
                if category.category == reward_category_relation.category.value:
                    cards_matrix[i][j] = RewardUnit.get_value(reward_category_relation.reward.reward_unit) * reward_category_relation.reward.amount
    
    return cards_matrix

# TODO doesn't use vendors yet
def create_wallet_matrix(user: User, heavy_hitters: HeavyHittersResponse) -> np.array:
    held_cards = user.credit_cards
    held_cards = [CreditCardSchema.model_validate(cc) for cc in held_cards] 

    return create_cards_matrix(held_cards, heavy_hitters)

# TODO doesn't use vendors
def create_heavy_hitter_matrix(heavy_hitters: HeavyHittersResponse) -> np.array:
    categories: List[HeavyHitterSchema] = heavy_hitters.categories
    vendors: List[HeavyHitterSchema] = heavy_hitters.vendors

    heavy_hitter_matrix = np.zeros((len(categories), len(categories)))
    for i, category in enumerate(categories):
        heavy_hitter_matrix[i][i] = category.amount

    return heavy_hitter_matrix


    







        