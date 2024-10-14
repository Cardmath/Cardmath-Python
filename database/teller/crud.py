from database.auth.user import Account, User
from database.teller.preferences import Preferences, CreditProfilePreferences, BanksPreferences, TravelPreferences, BusinessPreferences, ConsumerPreferences
from database.teller.transactions import Transaction, Counterparty, TransactionDetails
from datetime import datetime 
from sqlalchemy.orm import Session
import teller.schemas as schemas

def create_transaction(db: Session, transaction: schemas.TransactionSchema) -> Transaction:
    no_add = False
    db_txn = Transaction(
        txn_id = transaction.id,
        account_id = transaction.account_id,
        amount = transaction.amount,
        date = transaction.date,
        description = transaction.description,
        status = transaction.status,
        running_balance = transaction.running_balance,
        type = transaction.type)
        
    if transaction.details:
        db_txn_details = TransactionDetails(
        transaction=db_txn,
        processing_status=transaction.details.processing_status,
        category=transaction.details.category)
        
        db_counterparty = Counterparty()
        if transaction.details.counterparty:   
            counterparty_in_db = db.query(Counterparty).filter(
                Counterparty.name == transaction.details.counterparty.name and
                Counterparty.type == transaction.details.counterparty.type
                ).first()
            
            if counterparty_in_db is None:    
                db_counterparty = Counterparty(
                type=transaction.details.counterparty.type,
                name=transaction.details.counterparty.name)
            else :
                db_counterparty = counterparty_in_db
                no_add = True
        
    db_txn.details = db_txn_details
    
    db_txn_details.transaction = db_txn
    
    if db_txn_details.counterparty:
        db_txn_details.counterparty = db_counterparty
    
    db_counterparty.transaction_details.append(db_txn_details)
    
    if not no_add:
        db.add(db_txn)
        db.add(db_counterparty)
        db.add(db_txn_details)
        db.commit()
        db.refresh(db_txn)
    return db_txn

def create_account(db : Session, account : schemas.AccountSchema, schema=True) -> Account: 
    db_account = Account(
        id=account.id,
        enrollment_id = account.enrollment_id,
        institution_name = account.institution.name,
        institution_id = account.institution.id,
        type = account.type,
        name = account.name,
        subtype = account.subtype,
        currency = account.currency,
        last_four = account.last_four,
        status = account.status,
        last_updated = datetime.now()
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    
    if schema:
        return schemas.AccountSchema.from_db(db_account)
    return 

async def replace_credit_profile_preferences(user : User, db: Session, preferences: schemas.CreditProfileSchema) -> None:
    db_credit_profile = db.query(CreditProfilePreferences).filter_by(user_id=user.id).first()
    if db_credit_profile and schemas.CreditProfileSchema.model_validate(db_credit_profile):
        db.delete(db_credit_profile)
        print("[INFO] Replaced credit profile preferences.")
    else:
        print("[INFO] No credit profile preferences were found to replace.")
    
    credit_profile_preferences = CreditProfilePreferences(
        user_id = user.id,
        credit_score = preferences.credit_score,
        salary = preferences.salary,
        lifestyle = preferences.lifestyle
    )
    db.add(credit_profile_preferences)
    db.commit()
    db.refresh(credit_profile_preferences)
    return

async def replace_banks_preferences(user : User, db: Session, preferences: schemas.BanksPreferencesSchema) -> None:
    db_banks_preferences = db.query(BanksPreferences).filter_by(user_id=user.id).first()
    if db_banks_preferences and schemas.BanksPreferencesSchema.model_validate(db_banks_preferences):
        db.delete(db_banks_preferences)
        print("[INFO] Replaced banks preferences.")
    else:
        print("[INFO] No banks preferences were found to replace.")
    
    banks_preferences = BanksPreferences(
        user_id = user.id,
        have_banks = preferences.have_banks,
        preferred_banks = preferences.preferred_banks,
        avoid_banks = preferences.avoid_banks
    )
    db.add(banks_preferences)
    db.commit()
    db.refresh(banks_preferences)
    return

async def replace_travel_preferences(user : User, db: Session, preferences: schemas.TravelPreferencesSchema) -> None:
    db_travel_preferences = db.query(TravelPreferences).filter_by(user_id=user.id).first()
    if db_travel_preferences:
        db.delete(db_travel_preferences)
        print("[INFO] Replaced travel preferences.")
    else:
        print("[INFO] No travel preferences were found to replace.")
    
    airlines_preferences = TravelPreferences(
        user_id = user.id,
        preferred_airlines = preferences.preferred_airlines,
        avoid_airlines = preferences.avoid_airlines,
        frequent_travel_destinations = preferences.frequent_travel_destinations,
        desired_benefits = preferences.desired_benefits
    )

    db.add(airlines_preferences)
    db.commit()
    db.refresh(airlines_preferences)
    return airlines_preferences

async def replace_consumer_preferences(user : User, db: Session, preferences: schemas.ConsumerPreferencesSchema) -> None:
    db_consumer_preferences = db.query(ConsumerPreferences).filter_by(user_id=user.id).first()
    if db_consumer_preferences:
        db.delete(db_consumer_preferences)
        print("[INFO] Replaced consumer preferences.")
    else:
        print("[INFO] No consumer preferences were found to replace.")
    
    consumer_preferences = ConsumerPreferences(
        user_id = user.id,
        favorite_restaurants = preferences.favorite_restaurants,
        favorite_stores = preferences.favorite_stores
    )

    db.add(consumer_preferences)
    db.commit()
    db.refresh(consumer_preferences)
    return consumer_preferences

async def replace_business_preferences(user : User, db: Session, preferences: schemas.BusinessPreferencesSchema) -> None:
    db_business_preferences = db.query(BusinessPreferences).filter_by(user_id=user.id).first()
    if db_business_preferences :
        db.delete(db_business_preferences)
        print("[INFO] Replaced business preferences.")
    else:
        print("[INFO] No business preferences were found to replace.")
    
    business_preferences = BusinessPreferences(
        user_id = user.id,
        business_type = preferences.business_type,
        business_size = preferences.business_size
    )

    db.add(business_preferences)
    db.commit()
    db.refresh(business_preferences)
    return business_preferences

async def replace_preferences(user : User, db: Session, preferences: schemas.PreferencesSchema) -> None:
    db_preferences = user.preferences
    if db_preferences is None:
        db_preferences = Preferences(
            user_id = user.id,
            user = user
        )
        db.add(db_preferences)
        db.commit()
        db.refresh(db_preferences)
        # TODO validate the db preferences table
        # 
    print(preferences) 

    # We don't want to overwrite non-empty preferences with empty ones
    if preferences.credit_profile:
        await replace_credit_profile_preferences(user, db, preferences.credit_profile)
    if preferences.banks_preferences:
        await replace_banks_preferences(user, db, preferences.banks_preferences)
    if preferences.travel_preferences:
        await replace_travel_preferences(user, db, preferences.travel_preferences)
    if preferences.consumer_preferences:
        await replace_consumer_preferences(user, db, preferences.consumer_preferences)
    if preferences.business_preferences:
        await replace_business_preferences(user, db, preferences.business_preferences)

    return
