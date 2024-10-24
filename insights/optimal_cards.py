from creditcard.endpoints.read_database import read_credit_cards_database, CreditCardsDatabaseRequest
from creditcard.enums import * 
from creditcard.schemas import CreditCardSchema
from database.auth.user import User
from database.creditcard.creditcard import CreditCard
from insights.heavyhitters import read_heavy_hitters, HeavyHittersRequest, HeavyHittersResponse, HeavyHitterSchema
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from typing import Optional, List
from pyscipopt import Model, quicksum
from insights.schemas import MonthlyTimeframe

import numpy as np
from datetime import date

class OptimalCardsAllocationRequest(BaseModel):
    to_use: Optional[int] = 4
    to_add: Optional[int] = 0
    timeframe: Optional[MonthlyTimeframe] = None
    return_cards_used: Optional[bool] = False
    return_cards_added: Optional[bool] = False

class HeldCardsUseSummary(BaseModel):
    name: str
    value: float

class OptimalCardsAllocationResponse(BaseModel):
    total_reward_usd: float
    total_reward_allocation: List[int]
    summary: Optional[List[HeldCardsUseSummary]] = None
    cards_used: Optional[List[CreditCardSchema]] = None
    cards_added: Optional[List[CreditCardSchema]] = None

def create_cards_matrix(cards : List[CreditCardSchema], heavy_hitters: HeavyHittersResponse) -> np.array:
    categories: List[HeavyHitterSchema] = heavy_hitters.categories    
    vendors: List[HeavyHitterSchema] = heavy_hitters.vendors

    cards_matrix = np.zeros((len(categories), len(cards)))
    # TODO this is super inefficient but i am lazy rn
    for j, card in enumerate(cards):
        for i, category in enumerate(categories):
            for reward_category_relation in card.reward_category_map:
                if category.category == reward_category_relation.category.value:
                    cards_matrix[i][j] = RewardUnit.get_value(reward_category_relation.reward_unit) * reward_category_relation.amount
    
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

class RMatrixDetails(BaseModel):
    R: np.array 
    wallet_size: int
    add_size: int
    ccs_added: List[CreditCardSchema]
    ccs_used: List[CreditCardSchema]

    model_config = ConfigDict(arbitrary_types_allowed=True)


async def compute_r_matrix(db: Session, user: User, request: OptimalCardsAllocationRequest) -> RMatrixDetails:
    heavy_hitters_response: HeavyHittersResponse = await read_heavy_hitters(db=db, user=user, request=HeavyHittersRequest(account_ids="all", timeframe=request.timeframe))    
    W: np.array = create_wallet_matrix(user=user, heavy_hitters=heavy_hitters_response)
    wallet_size = W.shape[1]
    add_size = 0
    ccs_added = []
    if request.to_add > 0:
        cc_response = await read_credit_cards_database(db=db, request=CreditCardsDatabaseRequest(card_details="all"))
        ccs_added = cc_response.credit_card
        
        held_cards = user.credit_cards
        held_cards = [CreditCardSchema.model_validate(cc) for cc in held_cards] 
        ccs_added = [cc for cc in ccs_added if cc not in held_cards]
    
        ADD: np.array = create_cards_matrix(ccs_added, heavy_hitters=heavy_hitters_response)
        add_size = ADD.shape[1]
        W = np.hstack([W, ADD])
    H: np.array = create_heavy_hitter_matrix(heavy_hitters=heavy_hitters_response)
    R = W.T @ H
    return RMatrixDetails(R=R, wallet_size=wallet_size, add_size=add_size, ccs_added=ccs_added, ccs_used=[])

async def optimize_credit_card_selection_milp(db: Session, user: User, request: OptimalCardsAllocationRequest)  -> OptimalCardsAllocationResponse:
    rmatrix: RMatrixDetails = await compute_r_matrix(db=db, user=user, request=request)

    R = rmatrix.R
    wallet_size = rmatrix.wallet_size
    add_size = rmatrix.add_size

    print(f"[INFO] Wallet size: {wallet_size}, add size: {add_size}")

    wallet_indices: List[int] = np.arange(0, wallet_size)
    eligible_indices: List[int] = np.arange(wallet_size, add_size + wallet_size)
    assert len(wallet_indices) + len(eligible_indices) == R.shape[0]
    
    model = Model("credit_card_selection")

    if R.shape[0] == 0:
        print("[WARNING] R matrix is empty")
        return OptimalCardsAllocationResponse(total_reward_usd=0, total_reward_allocation=[], summary=[], cards_used=[], cards_added=[])

    C = len(R)
    H = len(R[0])

    x = {}
    for i in range(C):
        x[i] = model.addVar(vtype="B", name=f"x[{i}]")

    model.setObjective(
        quicksum(x[i] * R[i][j] for i in range(C) for j in range(H)),
        "maximize"
    )
    print(f"[INFO] C: {C}, H: {H}, wallet_size: {wallet_size}, add_size: {add_size}")
    if request.to_use > wallet_size:
        print("[WARNING] to_use > wallet_size")
        request.to_use = wallet_size

    model.addCons(quicksum(x[i] for i in range(C)) == request.to_use + request.to_add)
    model.addCons(quicksum(x[i] for i in wallet_indices) == request.to_use)
    model.addCons(quicksum(x[i] for i in eligible_indices) == request.to_add)

    model.optimize()

    selected_cards = [i for i in range(C) if model.getVal(x[i]) > 0.5]
    total_reward_usd = round(model.getObjVal(), 2)

    cards_added = []
    if request.return_cards_added:
        cards_added = [card for idx, card in enumerate(rmatrix.ccs_added) if idx + wallet_size in eligible_indices and idx + wallet_size in selected_cards]
        print(f"[INFO] {len(cards_added)} cards added of {len(eligible_indices)} eligible")

    cards_used = []
    if request.return_cards_used:
        cards_used = [CreditCardSchema.model_validate(cc) for cc in rmatrix.ccs_used]
    
    return OptimalCardsAllocationResponse(
        total_reward_usd=total_reward_usd,
        total_reward_allocation=selected_cards,
        summary=None,
        cards_used=cards_used,
        cards_added=cards_added)