from creditcard.schemas import WalletSchema, CardInWalletSchema
from database.auth.crud import update_user_enrollment
from database.auth.user import User, Enrollment, wallet_card_association
from database.creditcard.creditcard import CreditCard
from database.teller.crud import replace_preferences
from database.teller.transactions import Transaction
from sqlalchemy import select
from sqlalchemy.orm import aliased, Session
from teller.schemas import AccessTokenSchema, PreferencesSchema
from teller.utils import Teller, update_user_credit_cards, read_user_new_enrollment
from typing import List

async def process_new_enrollment(user: User, db: Session):
    '''
    After the initial sign-up, this function processes a new enrollment (<= 10 mins old) from the DB
    By fetching accounts, transactions from the Teller API and updating the user's credit cards
    '''
    teller_client = Teller()
    new_enrollments : List[Enrollment] = await read_user_new_enrollment(user=user, db=db)
    transactions : List[Transaction] = await teller_client.fetch_enrollment_transactions(db=db, enrollment=new_enrollments, should_categorize=True) 
    await update_user_credit_cards(user=user, db=db)
    
async def receive_teller_enrollment(user: User, access_token: AccessTokenSchema, db: Session):
    '''
    Adds a new enrollment to the user's account
    '''
    # TODO ensure the enrollment is not already in the db
    await update_user_enrollment(db=db, enrollment_schema=access_token, user_id=user.id)
    return

async def ingest_user_preferences(user: User, db: Session, preferences : PreferencesSchema):
    '''
    Updates the user's credit card preferences
    '''
    await replace_preferences(user=user, db=db, preferences=preferences)
    return

async def read_user_preferences(user: User) -> PreferencesSchema:
    '''
    Reads the user's credit card preferences
    '''
    if user.preferences is None:
        return PreferencesSchema()
    return PreferencesSchema.model_validate(user.preferences)

async def read_user_wallets(db: Session, user: User) -> List[WalletSchema]:
    if not user.wallets:
        return []

    wallets = []
    for wallet in user.wallets:
        cards_in_wallet = []

        # Use an alias to join the CreditCard and the association table fields
        card_alias = aliased(CreditCard)
        stmt = (
            select(
                wallet_card_association.c.is_held,
                wallet_card_association.c.wallet_id,
                wallet_card_association.c.credit_card_id,
                card_alias
            )
            .join(card_alias, wallet_card_association.c.credit_card_id == card_alias.id)
            .where(wallet_card_association.c.wallet_id == wallet.id)
        )

        results = db.execute(stmt).fetchall()

        # Populate CardInWalletSchema for each card in the wallet
        for row in results:
            cards_in_wallet.append(
                CardInWalletSchema(
                    is_held=row.is_held == "held",
                    credit_card_id=row.credit_card_id,
                    wallet_id=row.wallet_id,
                    card=row[3]  # the CreditCard object
                )
            )

        # Populate WalletSchema with cards
        wallets.append(
            WalletSchema(
                id=wallet.id,
                name=wallet.name,
                last_edited=wallet.last_edited,
                is_custom=wallet.is_custom,
                cards=cards_in_wallet
            )
        )

    return wallets