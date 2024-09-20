from database.auth.user import Account
from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Optional, List

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
        
class GetTransactionsResponse(BaseModel):
    number : int # number of transactions returned
    total_spend : Optional[int] = None # total amount spent
    transactions : Optional[List[TransactionSchema]] = None

    model_config = ConfigDict(from_attributes=True)
