from datetime import date
from datetime import date
from pydantic import BaseModel
from pydantic import BaseModel, field_validator, model_validator
from typing import List, Union, Optional, Tuple

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
        if v not in enums.PurchaseCategory:
            v = "unknown"
        return v

class HeavyHittersResponse(BaseModel):
    total: Optional[int] = None
    heavyhitters: List[HeavyHitterSchema]
    timeframe: MonthlyTimeframe

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