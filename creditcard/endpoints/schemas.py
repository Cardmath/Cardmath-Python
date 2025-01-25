from creditcard.enums import Benefit, CardAction, CreditCardKeyword, CreditNeeded, Issuer, List
from creditcard.schemas import CreditCardSchema
from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional, Union

class CreditCardRecommendationSchema(CreditCardSchema):
    status: CardAction

    @classmethod
    def from_credit_card_schema(cls, schema: CreditCardSchema, status: CardAction):
        return cls(**schema.model_dump(), status=status)


class CreditCardsFilter(BaseModel):
    id_in_db : Optional[List[int]]
    issuer : Optional[List[Issuer]]
    credit_needed : Optional[List[CreditNeeded]]
    benefits : Optional[List[Benefit]]
    keywords: Optional[List[CreditCardKeyword]]
    apr : Optional[float]


class CreditCardsDatabaseRequest(BaseModel):
    card_details: Union[str, CreditCardsFilter] = "all"
    use_preferences: bool
    max_num : Optional[int] = None

    @field_validator('card_details')
    @classmethod
    def validate_card_details(cls, v):
        if isinstance(v, str) and v != "all":
            raise ValueError('must be all or a filter')

        return v


class CardInWalletSchema(BaseModel):
    is_held : bool
    ccname: str
    ccissuer: str
    ccnetwork: str
    wallet_id: Optional[int]
    card : CreditCardSchema

    model_config = ConfigDict(from_attributes=True)


class WalletSchema(BaseModel):
    id : int
    name : str
    last_edited : date
    is_custom : bool
    cards: List[CardInWalletSchema]

    model_config = ConfigDict(from_attributes=True)


class CardLookupSchema(BaseModel):
    name: str
    issuer: str

    model_config = ConfigDict(from_attributes=True)


class WalletsIngestRequest(BaseModel):
    name : str
    cards : List[CardLookupSchema]
    is_custom : bool

    model_config = ConfigDict(from_attributes=True)


class WalletDeleteRequest(BaseModel):
    wallet_id: int


class WalletUpdateRequest(BaseModel):
    wallet_id: int
    name: Optional[str]
    is_custom: Optional[bool]
    cards: Optional[List[CardLookupSchema]]