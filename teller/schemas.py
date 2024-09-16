from datetime import date
from pydantic import BaseModel
from typing import Optional, List

class TellerUserSchema(BaseModel):
    id: str

class InstitutionSchema(BaseModel):
    name: str

class EnrollmentDetailsSchema(BaseModel):
    id: str
    institution: InstitutionSchema

class AccessTokenSchema(BaseModel):
    accessToken: str
    user: TellerUserSchema
    enrollment: EnrollmentDetailsSchema
    signatures: List[str]

    class Config:
        orm_mode = True

class CounterPartySchema(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None

    class Config:
        orm_mode = True

class TransactionDetailsSchema(BaseModel):
    processing_status: str
    category: Optional[str] = None
    counterparty: Optional[CounterPartySchema] = None
    
    class Config:
        orm_mode = True

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

    class Config:
        orm_mode = True