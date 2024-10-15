from creditcard.endpoints.read_database import read_credit_cards_database, CreditCardsDatabaseRequest
from creditcard.enums import * 
from creditcard.schemas import CreditCardSchema
from database.auth.user import User
from database.creditcard.creditcard import CreditCard
from insights.heavyhitters import read_heavy_hitters, HeavyHittersRequest, HeavyHittersResponse, HeavyHitterSchema
from pydantic import BaseModel 
from sqlalchemy.orm import Session
from typing import Optional, List
import numpy as np

class OptimalHeldCardsAllocationRequest(BaseModel):
    save_to_db: Optional[bool] = False

class HeldCardsUseSummary(BaseModel):
    name: str
    value: float

class OptimalHeldCardsAllocationResponse(BaseModel):
    total_reward_usd: float
    total_reward_allocation: List[int]
    summary: Optional[List[HeldCardsUseSummary]] = None

async def compute_optimal_held_cards_allocation(db: Session, user: User, request: OptimalHeldCardsAllocationRequest) -> OptimalHeldCardsAllocationResponse:
    heavy_hitters_response: HeavyHittersResponse = await read_heavy_hitters(db=db, user=user, request=HeavyHittersRequest(account_ids="all"))
    
    W: np.array = create_wallet_matrix(user=user, heavy_hitters=heavy_hitters_response) if request.add_to_wallet else None
    H: np.array = create_heavy_hitter_matrix(heavy_hitters=heavy_hitters_response)
    R = W.T @ H
    r = np.sum(np.max(R, axis=1))
    r_idx = np.argmax(R, axis=1)

    return OptimalHeldCardsAllocationResponse(total_reward_usd=r, total_reward_allocation=r_idx, summary=None)

def create_cards_matrix(cards : List[CreditCardSchema], heavy_hitters: HeavyHittersResponse) -> np.array:
    categories: List[HeavyHitterSchema] = heavy_hitters.categories    
    vendors: List[HeavyHitterSchema] = heavy_hitters.vendors

    cards_matrix = np.zeros((len(categories), len(cards)))
    # TODO this is super inefficient but i am lazy rn
    for j, card in enumerate(cards):
        for i, category in enumerate(categories):
            for reward_category_relation in card.reward_category_map:
                if category.name == reward_category_relation.category.name:
                    cards_matrix[i][j] = RewardUnit.get_value(reward_category_relation.reward.reward_unit) * reward_category_relation.reward.amount
    
    return cards_matrix

# TODO doesn't use vendors yet
def create_wallet_matrix(user: User, heavy_hitters: HeavyHittersResponse) -> np.array:
    held_cards = user.credit_cards.all()
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


    







        