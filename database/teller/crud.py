from database.auth.user import Account
from database.teller.transactions import Transaction, Counterparty, TransactionDetails
from datetime import datetime 
from sqlalchemy.orm import Session
from teller.schemas import TransactionSchema, AccountSchema

def create_transaction(db: Session, transaction: TransactionSchema) -> Transaction:
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
        
    db_txn.details = db_txn_details
    
    db_txn_details.transaction = db_txn
    
    if db_txn_details.counterparty:
        db_txn_details.counterparty = db_counterparty
    
    db_counterparty.transaction_details.append(db_txn_details)
    
    db.add(db_txn)
    db.add(db_counterparty)
    db.add(db_txn_details)
    db.commit()
    db.refresh(db_txn)
    return db_txn

def create_account(db : Session, account : AccountSchema, schema=True) -> Account: 
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
        return AccountSchema.from_db(db_account)
    
    return db_account