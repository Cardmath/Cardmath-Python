from auth.schemas import UserCreate
from database.auth.user import User, UserInDB, Enrollment, Account, Wallet, Subscription, wallet_card_association
from database.creditcard.creditcard import CreditCard
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy import insert
from sqlalchemy.orm import Session
from teller.schemas import AccessTokenSchema
from typing import List, Optional
from datetime import datetime

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, username: str) -> Optional[UserInDB]:
    return db.query(UserInDB).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_account_by_id(db: Session, account_id: str) -> Optional[Account]:
    return db.query(Account).filter(Account.id == account_id).first()

def create_user(db: Session, user: UserCreate):
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
    subscription = Subscription(
        user_id=db_user.id,
        status='unverified',
        start_date=None,
        end_date=None
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return db_user

def get_password_hash(password: str) -> str:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def update_user_password(db: Session, email: str, new_password: str) -> None:
    """
    Update the password of the user with the given email.
    """
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("User not found")
    
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)

async def update_user_enrollment(db: Session, enrollment_schema: AccessTokenSchema, user_id: int) -> Optional[Enrollment]:
    user = get_user(db=db, user_id=user_id)
    
    db_enrollment = Enrollment(
        id=enrollment_schema.enrollment.id,
        user_id=user_id,
        access_token=enrollment_schema.accessToken,
        institution_name=enrollment_schema.enrollment.institution.name,
        signatures=enrollment_schema.signatures,
        last_updated=datetime.now()
    )
    user.enrollments.append(db_enrollment)
    db.commit()
    db.refresh(user)
    
    return db_enrollment

async def update_user_with_credit_cards(db: Session, credit_cards: List[CreditCard], user_id: int, is_held: bool = True) -> Optional[User]:
    user = get_user(db, user_id)
    
    # Check if the user already has a wallet; if not, create one and commit to get its ID
    if not user.wallets:
        print("[INFO] Creating new wallet of held cards for user")
        new_wallet = Wallet(user_id=user_id, name="All Detected Cards", last_edited=datetime.today())
        db.add(new_wallet)
        db.commit()  # Commit to assign an ID to the wallet
        db.refresh(new_wallet)  # Refresh to get the wallet ID
        user.wallets.append(new_wallet)
    
    wallet = user.wallets[0]
    wallet.last_edited = datetime.today()
    wallet.is_custom = False

    # Ensure each credit card has an ID by adding it to the session and committing if necessary
    for credit_card in credit_cards:
        if credit_card.id is None:  # Add to session if not already in the database
            db.add(credit_card)
            db.commit()
            db.refresh(credit_card)

        # Now, add the card to the wallet association table with `is_held` status
        stmt = insert(wallet_card_association).values(
            wallet_id=wallet.id,
            credit_card_id=credit_card.id,
            is_held=True
        )
        db.execute(stmt)
        
        if not user.credit_cards:
            user.credit_cards = []

        # Also, associate credit card directly with user if needed
        if credit_card not in user.credit_cards:
            user.credit_cards.append(credit_card)

    db.commit()
    db.refresh(user)
    return user

def create_subscription(db: Session, user_id: int, status: str, duration_days: Optional[int] = 30, computations: Optional[int] = None) -> Subscription:
    """
    Create a new subscription for a user with given status, duration, and computation limit.
    """
    # Set the end date based on duration (e.g., 30 days by default)
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=duration_days) if duration_days else None

    subscription = Subscription(
        user_id=user_id,
        status=status,
        start_date=start_date,
        end_date=end_date,
        remaining_computations=computations
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription

def get_subscription_by_user_id(db: Session, user_id: int) -> Optional[Subscription]:
    """
    Retrieve the subscription for a specific user.
    """
    return db.query(Subscription).filter(Subscription.user_id == user_id).first()

def update_subscription_status(db: Session, user_id: int, status: str) -> Optional[Subscription]:
    """
    Update the subscription status and optionally the number of computations for a user.
    """
    subscription = get_subscription_by_user_id(db, user_id)
    if not subscription:
        return None

    subscription.status = status
    db.commit()
    db.refresh(subscription)
    return subscription

def delete_subscription(db: Session, user_id: int) -> None:
    """
    Delete a subscription for a user, if it exists.
    """
    subscription = get_subscription_by_user_id(db, user_id)
    if subscription:
        db.delete(subscription)
        db.commit()

def delete_user_data(user: User, db: Session):
    # Fetch and delete all enrollments associated with the user
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user.id).all()
    
    for enrollment in enrollments:
        db.delete(enrollment)
    
    db.commit()
    return {"msg": "User data deleted"}
