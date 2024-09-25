from sqlalchemy.orm import Session
from teller.schemas import AccessTokenSchema
from database.auth.user import User, Enrollment
from teller.utils import Teller, update_user_credit_cards, read_user_new_enrollment
from database.teller.transactions import Transaction
from typing import List
from database.auth.crud import update_user_enrollment

async def process_new_enrollment(user: User, db: Session):
    '''
    After the initial sign-up, this function processes a new enrollment (<= 10 mins old) from the DB
    By fetching accounts, transactions from the Teller API and updating the user's credit cards
    '''
    teller_client = Teller()
    new_enrollments : List[Enrollment] = await read_user_new_enrollment(user=user, db=db)
    transactions : List[Transaction] = await teller_client.fetch_enrollment_transactions(db=db, enrollment=new_enrollments) 
    await update_user_credit_cards(user=user, db=db)
    
async def receive_teller_enrollment(user: User, access_token: AccessTokenSchema, db: Session):
    '''
    Adds a new enrollment to the user's account
    '''
    # TODO ensure the enrollment is not already in the db
    await update_user_enrollment(db=db, enrollment_schema=access_token, user_id=user.id)
    return

