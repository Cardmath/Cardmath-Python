from auth.schemas import UserCreate
from database.auth.user import User, UserInDB, Enrollment
from database.creditcard.creditcard import CreditCard
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from teller.schemas import AccessTokenSchema
from typing import List, Optional

from datetime import datetime

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[UserInDB]:
    return db.query(UserInDB).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> UserInDB:
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_password_hash(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

async def update_user_enrollment(db: Session, enrollment_schema: AccessTokenSchema, user_id: int) -> Optional[Enrollment]:
    user = get_user(db=db, user_id=user_id)
    
    db_enrollment = Enrollment(
        user_id=user_id,
        access_token=enrollment_schema.accessToken,
        enrollment_id=enrollment_schema.enrollment.id,
        institution_name=enrollment_schema.enrollment.institution.name,
        signatures=enrollment_schema.signatures,
        last_updated=datetime.now()
    )
    user.enrollments.append(db_enrollment)
    db.commit()
    db.refresh(user)
    
    return db_enrollment

async def update_user_with_credit_cards(db : Session, credit_cards : List[CreditCard], user_id : int) -> Optional[User]:
    user = get_user(db, user_id)
    for credit_card in credit_cards:
        user.credit_cards.append(credit_card)
    db.commit()
    db.refresh(user)
    return user