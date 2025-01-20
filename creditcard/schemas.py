from collections import defaultdict
from creditcard.enums import *  
from creditcard.enums import CardKey
from database.creditcard.creditcard import CreditCard
from pydantic import BaseModel, ConfigDict, TypeAdapter, Field
from typing import List
from typing import Optional, Union
from creditcard.enums import *
from creditcard.enums import CardKey
from pydantic import BaseModel, ConfigDict, field_validator, field_serializer, model_validator
from typing import List, Union, Optional, Any
from datetime import timedelta, date

RIGHTS_RESERVED = '\u00AE'

class RewardCategoryThreshold(BaseModel):
    on_up_to_purchase_amount_usd: float
    per_timeframe_num_months: int
    fallback_reward_amount: float

    model_config = ConfigDict(from_attributes=True)

    @field_validator('fallback_reward_amount', mode="before")
    @classmethod
    def amount_must_be_reasonable(cls, v):
        if v < 0 or v > 10:
            raise ValueError('Amount must be positive and less than 20 to be reasonable')
        return v

class RewardCategoryRelation(BaseModel):
    category : Union[PurchaseCategory, Vendors]
    reward_unit : RewardUnit
    reward_amount : float

    reward_threshold : Optional[RewardCategoryThreshold] = None
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator('reward_amount', mode="before")
    @classmethod
    def amount_must_be_reasonable(cls, v):
        if v < 0 or v > 30:
            raise ValueError('Amount must be positive and less than 30 to be reasonable')
        return v
    
    @field_validator('reward_threshold', mode="before")
    @classmethod
    def validate_threshold(cls, v):
        if v is not None:
            v = RewardCategoryThreshold.model_validate(v)
            if v.on_up_to_purchase_amount_usd < 0 or v.per_timeframe_num_months < 0:
                return None
            else :
                return v

class RewardCategoryMap(BaseModel):
    reward_category_map : List[RewardCategoryRelation]

    def get_primary_reward_unit(self) -> RewardUnit:
        if len(self.reward_category_map) == 0:
            return RewardUnit.UNKNOWN
        
        reward_unit_counts = defaultdict(int)
        
        for relation in self.reward_category_map:
            reward_unit_counts[relation.reward_unit] += 1
        
        primary_reward_unit = max(reward_unit_counts, key=reward_unit_counts.get)
        return primary_reward_unit


class ConditionalSignOnBonus(BaseModel):
    purchase_type: Union[PurchaseCategory, Vendors]
    condition_amount: float
    timeframe: timedelta

    reward_type: RewardUnit
    reward_amount: float

    model_config = ConfigDict(from_attributes=True)

    @field_validator('timeframe', mode="before")
    @classmethod
    def parse_as_months(cls, v):
        if isinstance(v, (int, float)):
            return timedelta(days=30 * v)
        return v

    @field_serializer('timeframe')
    @classmethod
    def serialize_as_months(cls, v):
        if isinstance(v, timedelta):
            return v.days / 30
        
    def get_timeframe_in_months(self):
        return self.timeframe.days / 30

class APR(BaseModel):
    apr : float
    apr_type : APRType
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator('apr', mode="before")
    def apr_must_be_reasonable(cls, v):
        if v < 0 or v > 100:
            raise ValueError('APR must be positive and less than 100 to be reasonable')
        return v 

class AnnualFee(BaseModel):
    fee_usd : float
    waived_for : int

    model_config = ConfigDict(from_attributes=True)

    @field_validator('fee_usd')
    def fee_usd_must_be_reasonable(cls, v):
        if v < 0:
            raise ValueError('Fee must be positive to be reasonable')
        return v
    
    @field_validator('waived_for')
    def waived_for_must_be_reasonable(cls, v):
        if v < 0:
            raise ValueError('Waived for must be positive to be reasonable')
        return v

class PeriodicStatementCredit(BaseModel): 
    credit_amount: float
    unit: RewardUnit 
    categories: List[PurchaseCategory] # purchase categories where the statement credit can be used
    vendors: List[Vendors] # stores where the statement credit can be used
    timeframe_months: int
    max_uses: int

    description: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator('timeframe_months', mode="before")
    def timeframe_must_be_reasonable(cls, v):
        if v < 0:
            raise ValueError('Timeframe must be positive to be reasonable')
        return v

class CreditCardKeyMetadata(BaseModel):
    name: str
    issuer: Issuer
    network: Network
    key: Optional[CardKey]

class CreditCardMetadataSchema(CreditCardKeyMetadata):
    last_verified: Optional[date] # None means never verified
    referral_link: Optional[str]

class CreditCardSourceMetadataSchema(CreditCardKeyMetadata):
    reference_links: Optional[str]
    source_last_verified: Optional[date] # None means never verified
        
class CreditCardSchema(BaseModel):
    name: str
    issuer: Issuer
    network: Network

    key: Optional[CardKey]
    last_verified: Optional[date] # None means never verified
    referral_link: Optional[str]
    
    reward_category_map : List[RewardCategoryRelation]
    benefits : List[Benefit]
    credit_needed : List[CreditNeeded]
    apr : List[APR]
    sign_on_bonus : Optional[List[ConditionalSignOnBonus]] = None
    annual_fee: Optional[AnnualFee] = None
    statement_credit: List[PeriodicStatementCredit]
    primary_reward_unit: RewardUnit
    keywords: List[CreditCardKeyword]

    model_config=ConfigDict(from_attributes=True)

    def __hash__(self):
        return hash((self.name, self.issuer, self.network))
    
    def __eq__(self, other):
        if not isinstance(other, CreditCardSchema):
            return False
        return hash(self) == hash(other)

    def credit_card(self) -> CreditCard:
        return CreditCard(name=self.name, 
                          issuer=self.issuer,
                          network=self.network,
                          benefits=TypeAdapter(List[Benefit]).dump_python(self.benefits),
                          credit_needed=TypeAdapter(List[CreditNeeded]).dump_python(self.credit_needed),
                          reward_category_map=TypeAdapter(List[RewardCategoryRelation]).dump_python(self.reward_category_map),
                          sign_on_bonus=TypeAdapter(List[ConditionalSignOnBonus]).dump_python(self.sign_on_bonus),
                          apr=TypeAdapter(List[APR]).dump_python(self.apr),
                          annual_fee = self.annual_fee.model_dump(),
                          keywords= TypeAdapter(List[CreditCardKeyword]).dump_python(self.keywords),
                          statement_credit=TypeAdapter(List[PeriodicStatementCredit]).dump_python(self.statement_credit),
                          primary_reward_unit=self.primary_reward_unit)