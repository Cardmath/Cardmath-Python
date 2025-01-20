from creditcard.endpoints.schemas import CardLookupSchema, CreditCardRecommendationSchema
from creditcard.schemas import CreditCardSchema, RewardCategoryRelation
from datetime import date
from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing import List, Union, Optional, Tuple, Dict
import creditcard.enums as enums
from teller.schemas import TransactionSchema
import numpy as np

import creditcard.enums as enums

import re

class MonthlyTimeframe(BaseModel):
    start_month: date
    end_month: date

    @model_validator(mode="before")
    @classmethod
    def validate_timeframe(cls, values):
         
        if isinstance(values, dict):
            start_month = values.get('start_month')
            end_month = values.get('end_month')

            if isinstance(start_month, str) and isinstance(end_month, str):
                values['start_month'] = date.fromisoformat(start_month).replace(day=1)
                start_month = values['start_month']

                values['end_month'] = date.fromisoformat(end_month).replace(day=1)
                end_month = values['end_month']

            if start_month and end_month:
                if end_month < start_month:
                    raise ValueError("End month must be after start month")
                if start_month > date.today():
                    raise ValueError("Start month must be in the past")
        return values

class HeavyHittersRequest(BaseModel):
    account_ids: Union[str, List[str]]
    top_n: int = None # if none then all    
    timeframe: Optional[MonthlyTimeframe] = None 

    @field_validator("top_n")
    @classmethod
    def top_n_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('must be positive')
        return v

VENDOR_CONST = "VENDOR"
CATEGORY_CONST = "CATEGORY"
class HeavyHitterSchema(BaseModel):
    type: str # VENDOR or CATEGORY
    name: Optional[enums.Vendors] = None
    category: str
    percent: str 
    amount: float

    @field_validator("type")
    @classmethod
    def type_is_vendor_or_category(cls, v):
        if v is not None and v is not VENDOR_CONST and v is not CATEGORY_CONST:
            raise ValueError('must be either a vendor or a category')
        return v
    
    @field_validator("percent")
    @classmethod
    def validate_percentage(cls, percentage_str):
        # Regular expression for a percentage (e.g., "85%", "85.00%", "100%", "0%", "0.5%")
        pattern = r"^(100(\.0{1,2})?|[0-9]{1,2}(\.[0-9]{1,2})?)%$"
        
        if re.match(pattern, percentage_str):
            return percentage_str
        else:
            raise ValueError('must be a percentage')
    
    @field_validator("category", mode="before")
    @classmethod
    def category_is_valid(cls, v):
        # Check if the provided value `v` is a valid PurchaseCategory value
        if v not in {category.value for category in enums.PurchaseCategory}:
            v = enums.PurchaseCategory.UNKNOWN
        return v
    
class CategorizationProgressSummary(BaseModel):
    categorized_cc_eligible_count: int
    uncategorized_cc_eligible_count: int
    non_cc_eligible_count: int

class HeavyHittersResponse(BaseModel):
    total: Optional[int] = None
    heavyhitters: List[HeavyHitterSchema]
    timeframe: Optional[MonthlyTimeframe]
    categorization_progress_summary: CategorizationProgressSummary

    @field_validator("total")
    @classmethod
    def total_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('must be positive')
        return v
    
class CategoriesMovingAveragesRequest(BaseModel):
    account_ids: Union[str, List[str]] # if "all" then all accounts associated with user
    date_range: Optional[Tuple[date, date]] = None # if none then entire time
    window_size: int = 7
    top_n: int = None # if none then all

    @field_validator("top_n")
    @classmethod
    def top_n_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('must be positive')
        return v
    
    @field_validator("window_size")
    @classmethod
    def window_size_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('must be positive')
        return v

    @field_validator("account_ids")
    @classmethod
    def account_ids_must_be_all_or_list_of_ids(cls, v):
        if v is not None and v != "all" and not isinstance(v, list):
            raise ValueError('must be all or a list of ids')
        return v

class MovingAveragesSeries(BaseModel):
    name: str
    moving_average: List[float]

class CategoriesMovingAveragesResponse(BaseModel):
    categories: List[MovingAveragesSeries]
    dates: List[date]

    @model_validator(mode="before")
    @classmethod
    def all_series_must_have_same_length(cls, values):
        categories = values.get('categories')
        dates = values.get('dates')
        if categories is not None and dates is not None:
            for c in categories:
                if len(c.moving_average) != len(dates):
                    raise ValueError('all series must have the same number of amounts as dates')
        return values

class OptimalCardsAllocationCardLookupSchema(BaseModel):
    is_new: bool = False # if true then card is new and should consider sign on bonus (sob)
    card: CardLookupSchema

class OptimalCardsAllocationRequestWalletOverride(BaseModel):
    name: str
    cards: List[OptimalCardsAllocationCardLookupSchema]

class OptimalCardsAllocationRequest(BaseModel):
    num_solutions: int = 5

    wallet_override: Optional[OptimalCardsAllocationRequestWalletOverride] = None

    to_use: Optional[int] = 4
    to_add: Optional[int] = 0

    timeframe: Optional[MonthlyTimeframe] = None
    use_sign_on_bonus: bool = False
    return_cards_used: Optional[bool] = False
    use_all_wallet_cards: Optional[bool] = False
    return_cards_added: Optional[bool] = False
    return_cards_dropped: Optional[bool] = False

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

class OptimalCardsAllocationSolution(BaseModel):
    timeframe: MonthlyTimeframe
    total_reward_usd: float
    total_regular_rewards_usd: float
    total_sign_on_bonus_usd: float
    total_statement_credits_usd: float
    total_annual_fees_usd: float
    net_rewards_usd: float

    total_reward_allocation: List[int]
    summary: Optional[List[CardsUseSummary]] = None
    spending_plan: Optional[List[SpendingPlanItem]] = None

    cards_used: Optional[List[CreditCardRecommendationSchema]] = None
    cards_added: Optional[List[CreditCardRecommendationSchema]] = None
    cards_dropped: Optional[List[CreditCardRecommendationSchema]] = None

class OptimalCardsAllocationResponse(BaseModel):
    timeframe: MonthlyTimeframe
    solutions: List[OptimalCardsAllocationSolution]

class RMatrixDetails(BaseModel):
    R: np.array
    wallet_size: int
    
    to_add: int
    ccs_added: List[CreditCardSchema]
    
    to_use: int 
    ccs_used: List[CreditCardSchema]

    card_sob_data: dict
    annual_fees: List[float]
    annual_statement_credits: List[float]
    
    timeframe: MonthlyTimeframe
    categories: List[str]
    card_names: List[str]
    reward_relations: Dict[Tuple[str, str], RewardCategoryRelation]
    heavy_hitter_vector: np.array
    M : float 

    model_config = ConfigDict(arbitrary_types_allowed=True)