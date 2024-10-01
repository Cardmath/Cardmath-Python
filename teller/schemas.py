from database.auth.user import Account
from datetime import date
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing import Optional, List

import creditcard.enums as enums

class TellerUserSchema(BaseModel):
    id: str

class InstitutionSchema(BaseModel):
    name: str

class EnrollmentDetailsSchema(BaseModel):
    id: str
    institution: InstitutionSchema
    
class InstitutionSchema(BaseModel):
    name : str
    id : str

class LinksSchema(BaseModel):
    balances: str
    self: str
    transactions: str

class AccountSchema(BaseModel):
    enrollment_id : str
    links : Optional[LinksSchema] = None
    institution: InstitutionSchema
    type: str
    name: str
    subtype: str
    currency: str
    id: str
    last_four: str
    status: str

    def from_db(account : Account):
        return AccountSchema(
            id=account.id,
            enrollment_id=account.enrollment_id,
            institution=InstitutionSchema(name=account.institution_name, id=account.institution_id),
            type = account.type,
            name = account.name,
            subtype = account.subtype,
            currency = account.currency,
            last_four=account.last_four,
            status=account.status
        )
        
class AccessTokenSchema(BaseModel):
    accessToken: str
    user: TellerUserSchema
    enrollment: EnrollmentDetailsSchema
    signatures: List[str]

    model_config = ConfigDict(from_attributes=True)

class CounterPartySchema(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TransactionDetailsSchema(BaseModel):
    processing_status: str
    category: Optional[str] = None
    counterparty: Optional[CounterPartySchema] = None

    model_config = ConfigDict(from_attributes=True)

class TransactionSchema(BaseModel):
    description: str
    date: date
    account_id: str
    amount: float
    status: str
    id : str
    type : str
    running_balance: Optional[str] = None 
    details: TransactionDetailsSchema

    model_config = ConfigDict(from_attributes=True)

class CreditProfileSchema(BaseModel):
    credit_score : Optional[int] = None
    salary : Optional[int] = None
    lifestyle : Optional[enums.Lifestyle] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('credit_score')
    @classmethod
    def credit_score_must_be_between_300_and_850(cls, v):
        if v is not None and (v < 300 or v > 850):
            raise ValueError('must be between 300 and 850')
        return v
    
    @field_validator('salary')
    @classmethod
    def salary_positive(cls, v):
        if v is not None and v < 0:
            raise ValueError('must be positive')
        return v

class BanksPreferencesSchema(BaseModel):
    have_banks : Optional[List[enums.Issuer]] = None
    preferred_banks : Optional[List[enums.Issuer]] = None
    avoid_banks : Optional[List[enums.Issuer]] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    @model_validator(mode="before")
    def no_intersection(cls, data):
        print(data)
        if isinstance(data, dict):
            if len(set(data.get('preferred_banks')).intersection(data.get('have_banks'))) != 0:
                raise ValueError('have_banks and avoid_banks cannot be used together')
            if len(set(data.get('preferred_banks')).intersection(data.get('have_banks'))) != 0:
                raise ValueError('preferred_banks and avoid_banks cannot be used together')
            if len(set(data.get('preferred_banks')).intersection(data.get('have_banks'))) != 0:
                raise ValueError('preferred_banks and have_banks cannot be used together')
            
        # TODO decide how to resolve intersections
            
        return data
    
class TravelPreferencesSchema(BaseModel):
    preferred_airlines : Optional[List[enums.Airline]] = None
    avoid_airlines : Optional[List[enums.Airline]] = None
    frequent_travel_destinations : Optional[List[str]] = None
    desired_benefits : Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)
    
class ConsumerPreferencesSchema(BaseModel):
    favorite_restaurants : Optional[List[str]] = None
    favorite_stores : Optional[List[str]] = None

    model_config = ConfigDict(strict=True, from_attributes=True)


class BusinessPreferencesSchema(BaseModel):
    business_type : Optional[enums.BusinessType] = None
    business_size : Optional[enums.BusinessSize] = None

    model_config = ConfigDict(strict=True, from_attributes=True)

class PreferencesSchema(BaseModel):
    credit_profile : Optional[CreditProfileSchema] = None
    banks_preferences : Optional[BanksPreferencesSchema] = None
    travel_preferences : Optional[TravelPreferencesSchema] = None
    consumer_preferences : Optional[ConsumerPreferencesSchema] = None
    business_preferences : Optional[BusinessPreferencesSchema] = None

    model_config = ConfigDict(from_attributes=True)