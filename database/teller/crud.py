from database.auth.user import Account, User, Enrollment
from database.teller.preferences import Preferences, CreditProfilePreferences, BanksPreferences, RewardsProgramsPreferences, BusinessPreferences, ConsumerPreferences
from database.teller.transactions import Transaction, Counterparty, TransactionDetails
from datetime import datetime 
from sqlalchemy import exists
from sqlalchemy.orm import Session
from typing import List
import teller.schemas as schemas

def read_user_enrollments(user: User, db: Session) -> List[Enrollment]:
    '''
    Reads all of a user's enrollments from the DB
    '''
    enrollments = db.query(Enrollment).filter(Enrollment.user_id == user.id).all()
    return enrollments

def create_transaction(
    db: Session, 
    account: Account, 
    transaction: schemas.TransactionSchema,
    bulk_mode: bool = False,
    skip_exists_check: bool = False
) -> Transaction:
    """
    Create a transaction record in the database.
    
    Args:
        db: Database session
        account: Account associated with the transaction
        transaction: Transaction data
        bulk_mode: If True, don't commit (caller will handle commit)
        skip_exists_check: If True, skip checking if transaction exists
    """
    if transaction.account_id != account.id:
        print("[CRITICAL ERROR] Transaction account id does not match account id")
        return None

    # Check for existing transaction unless explicitly skipped
    if not skip_exists_check:
        txn_with_id = db.query(Transaction).filter(Transaction.txn_id == transaction.txn_id).first()
        if txn_with_id:
            return None
         
    db_txn = Transaction(
        account=account,
        txn_id=transaction.txn_id,
        amount=transaction.amount,
        date=transaction.date,
        description=transaction.description,
        status=transaction.status,
        running_balance=transaction.running_balance,
        type=transaction.type
    )
        
    if transaction.details:
        db_txn_details = TransactionDetails(
            transaction=db_txn,
            processing_status=transaction.details.processing_status,
            category=transaction.details.category
        )
        
        db_counterparty = Counterparty()
        if transaction.details.counterparty:   
            counterparty_in_db = db.query(Counterparty).filter(
                (Counterparty.name == transaction.details.counterparty.name) &
                (Counterparty.type == transaction.details.counterparty.type)
            ).first()
            
            if counterparty_in_db is None:    
                db_counterparty = Counterparty(
                    type=transaction.details.counterparty.type,
                    name=transaction.details.counterparty.name
                )
            else:
                db_counterparty = counterparty_in_db
        
    db_txn.details = db_txn_details
    db_txn_details.transaction = db_txn
    
    if db_txn_details.counterparty:
        db_txn_details.counterparty = db_counterparty
    
    db_counterparty.transaction_details.append(db_txn_details)
    
    db.add(db_txn)
    db.add(db_counterparty)
    db.add(db_txn_details)

    if not bulk_mode:
        db.commit()
        db.refresh(db_txn)

    return db_txn

def create_transactions_bulk(
    db: Session,
    account: Account,
    transactions: List[schemas.TransactionSchema],
    batch_size: int = 100,
    is_new_user: bool = False
) -> List[Transaction]:
    """
    Bulk create transactions with batching for better performance.
    For new users, skips existence checks for better performance.
    """
    if not transactions:
        return []

    # For existing users, check if any transactions exist
    if not is_new_user:
        txn_ids = [t.txn_id for t in transactions]
        exists_query = db.query(exists().where(Transaction.txn_id.in_(txn_ids))).scalar()
        skip_exists_check = not exists_query
    else:
        skip_exists_check = True

    created_transactions = []
    
    for i in range(0, len(transactions), batch_size):
        batch = transactions[i:i + batch_size]
        for transaction in batch:
            txn = create_transaction(
                db, 
                account, 
                transaction, 
                bulk_mode=True,
                skip_exists_check=skip_exists_check
            )
            if txn:
                created_transactions.append(txn)
        
        try:
            db.commit()
            print(f"Committed batch {i//batch_size + 1}, {len(created_transactions)} transactions so far")
        except Exception as e:
            db.rollback()
            print(f"Error in batch {i//batch_size + 1}: {str(e)}")
            raise

    return created_transactions

# Rest of your existing code remains the same...

def create_account(db: Session, account: schemas.AccountSchema) -> Account: 
    db_account = Account(
        id=account.id,
        enrollment_id=account.enrollment_id,
        institution_name=account.institution.name,
        institution_id=account.institution.id,
        type=account.type,
        name=account.name,
        subtype=account.subtype,
        currency=account.currency,
        last_four=account.last_four,
        status=account.status,
        last_updated=datetime.now()
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    
    return db_account

def replace_credit_profile_preferences(user: User, db: Session, preferences: schemas.CreditProfileSchema) -> None:
    db_credit_profile = db.query(CreditProfilePreferences).filter_by(user_id=user.id).first()
    if db_credit_profile and schemas.CreditProfileSchema.model_validate(db_credit_profile):
        db.delete(db_credit_profile)
        print("[INFO] Replaced credit profile preferences.")
    else:
        print("[INFO] No credit profile preferences were found to replace.")
    
    credit_profile_preferences = CreditProfilePreferences(
        user_id=user.id,
        credit_score=preferences.credit_score,
        salary=preferences.salary,
        lifestyle=preferences.lifestyle
    )
    db.add(credit_profile_preferences)
    db.commit()
    db.refresh(credit_profile_preferences)

def replace_banks_preferences(user: User, db: Session, preferences: schemas.BanksPreferencesSchema) -> None:
    db_banks_preferences = db.query(BanksPreferences).filter_by(user_id=user.id).first()
    if db_banks_preferences and schemas.BanksPreferencesSchema.model_validate(db_banks_preferences):
        db.delete(db_banks_preferences)
        print("[INFO] Replaced banks preferences.")
    else:
        print("[INFO] No banks preferences were found to replace.")
    
    banks_preferences = BanksPreferences(
        user_id=user.id,
        have_banks=preferences.have_banks,
        preferred_banks=preferences.preferred_banks,
        avoid_banks=preferences.avoid_banks
    )
    db.add(banks_preferences)
    db.commit()
    db.refresh(banks_preferences)

def replace_rewards_programs_preferences(user: User, db: Session, preferences: schemas.RewardsProgramsPreferencesSchema) -> None:
    db_travel_preferences = db.query(RewardsProgramsPreferences).filter_by(user_id=user.id).first()
    if db_travel_preferences:
        db.delete(db_travel_preferences)
        print("[INFO] Replaced travel preferences.")
    else:
        print("[INFO] No travel preferences were found to replace.")
    
    airlines_preferences = RewardsProgramsPreferences(
        user_id=user.id,
        preferred_rewards_programs=preferences.preferred_rewards_programs,
        avoid_rewards_programs=preferences.avoid_rewards_programs
    )

    db.add(airlines_preferences)
    db.commit()
    db.refresh(airlines_preferences)
    return airlines_preferences

def replace_consumer_preferences(user: User, db: Session, preferences: schemas.ConsumerPreferencesSchema) -> None:
    db_consumer_preferences = db.query(ConsumerPreferences).filter_by(user_id=user.id).first()
    if db_consumer_preferences:
        db.delete(db_consumer_preferences)
        print("[INFO] Replaced consumer preferences.")
    else:
        print("[INFO] No consumer preferences were found to replace.")
    
    consumer_preferences = ConsumerPreferences(
        user_id=user.id,
        favorite_grocery_stores=preferences.favorite_grocery_stores,
        favorite_general_goods_stores=preferences.favorite_general_goods_stores
    )

    db.add(consumer_preferences)
    db.commit()
    db.refresh(consumer_preferences)
    print(f"Consumer preferences: {preferences}")
    return consumer_preferences

def replace_business_preferences(user: User, db: Session, preferences: schemas.BusinessPreferencesSchema) -> None:
    db_business_preferences = db.query(BusinessPreferences).filter_by(user_id=user.id).first()
    if db_business_preferences:
        db.delete(db_business_preferences)
        print("[INFO] Replaced business preferences.")
    else:
        print("[INFO] No business preferences were found to replace.")
    
    business_preferences = BusinessPreferences(
        user_id=user.id,
        business_type=preferences.business_type,
        business_size=preferences.business_size
    )

    db.add(business_preferences)
    db.commit()
    db.refresh(business_preferences)
    return business_preferences

def replace_preferences(user: User, db: Session, preferences: schemas.PreferencesSchema) -> None:
    db_preferences = user.preferences
    if db_preferences is None:
        db_preferences = Preferences(
            user_id=user.id,
        )
        db.add(db_preferences)
        db.commit()
        db.refresh(db_preferences)

    # We don't want to overwrite non-empty preferences with empty ones
    if preferences.credit_profile:
        replace_credit_profile_preferences(user, db, preferences.credit_profile)
    if preferences.banks_preferences:
        replace_banks_preferences(user, db, preferences.banks_preferences)
    if preferences.rewards_programs_preferences:
        print(preferences.rewards_programs_preferences)
        replace_rewards_programs_preferences(user, db, preferences.rewards_programs_preferences)
    if preferences.consumer_preferences:
        replace_consumer_preferences(user, db, preferences.consumer_preferences)
    if preferences.business_preferences:
        replace_business_preferences(user, db, preferences.business_preferences)