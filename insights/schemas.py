from pydantic import BaseModel, field_validator
from typing import List, Union, Optional

class HeavyHittersRequest(BaseModel):
    account_ids: Union[str, List[str]]
    top_n: int = None # if none then all     

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
    name: Optional[str] = None
    category: str
    percent: float = None

    @field_validator("type")
    @classmethod
    def type_is_vendor_or_category(cls, v):
        if v is not None and v is not VENDOR_CONST and v is not CATEGORY_CONST:
            raise ValueError('must be either a vendor or a category')
        return v
    
    @field_validator("percent")
    @classmethod
    def percent_must_be_between_0_and_100(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('must be between 0 and 100')
        return v

class HeavyHittersResponse(BaseModel):
    total: Optional[int] = None
    categories: List[HeavyHitterSchema]
    vendors: List[HeavyHitterSchema]

    @field_validator("total")
    @classmethod
    def total_must_be_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('must be positive')
        return v

