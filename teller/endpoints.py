from creditcard.endpoints.schemas import CardInWalletSchema, WalletDeleteRequest, WalletSchema, WalletsIngestRequest
from creditcard.endpoints.schemas import WalletUpdateRequest
from database.auth.crud import update_user_enrollment
from database.auth.user import User, Wallet, wallet_card_association
from database.creditcard.creditcard import CreditCard
from database.teller.crud import replace_preferences
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import aliased, Session
from teller.schemas import AccessTokenSchema, PreferencesSchema
from teller.utils import Teller, update_user_credit_cards, read_user_new_enrollment
from typing import List

def process_new_enrollment(user: User, db: Session):
    '''
    After the initial sign-up, this function processes a new enrollment (<= 10 mins old) from the DB
    By fetching accounts, transactions from the Teller API and updating the user's credit cards
    '''
    teller_client = Teller()
    new_enrollments = read_user_new_enrollment(user=user, db=db)
    transactions = teller_client.fetch_enrollment_transactions(db=db, enrollment=new_enrollments, should_categorize=True) 
    update_user_credit_cards(user=user, db=db)
    
def receive_teller_enrollment(user: User, access_token: AccessTokenSchema, db: Session):
    '''
    Adds a new enrollment to the user's account
    '''
    # TODO ensure the enrollment is not already in the db
    update_user_enrollment(db=db, enrollment_schema=access_token, user_id=user.id)
    return

def ingest_user_preferences(user: User, db: Session, preferences: PreferencesSchema):
    '''
    Updates the user's credit card preferences
    '''
    replace_preferences(user=user, db=db, preferences=preferences)
    return

def read_user_preferences(user: User) -> PreferencesSchema:
    '''
    Reads the user's credit card preferences
    '''
    if user.preferences is None:
        return PreferencesSchema()
    return PreferencesSchema.model_validate(user.preferences)

def read_user_wallets(db: Session, user: User) -> List[WalletSchema]:
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

def ingest_user_wallet(user: User, db: Session, wallet: WalletsIngestRequest) -> WalletSchema:
    # Validate and fetch each credit card by name and issuer
    valid_cards = []
    for card in wallet.cards:
        db_card = db.query(CreditCard).filter_by(name=card.name, issuer=card.issuer).first()
        if not db_card:
            raise HTTPException(status_code=400, detail=f"Credit card {card.name} by {card.issuer} not found.")
        
        valid_cards.append(db_card)  # Collect ORM instances directly

    # Create new wallet entry without associating cards yet
    new_wallet = Wallet(
        user_id=user.id,
        name=wallet.name,
        last_edited=datetime.today(),
        is_custom=wallet.is_custom
    )
    
    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)  # Get the wallet ID after commit

    # Associate the valid ORM card instances with the new wallet
    new_wallet.cards = valid_cards  # Assign the ORM instances directly

    # Commit the final wallet and card association
    db.commit()
    db.refresh(new_wallet)

    # Convert the new_wallet to WalletSchema for response with CardInWalletSchema details
    card_in_wallet_schemas = [
        CardInWalletSchema(
            is_held=False,  # Or set based on your logic
            credit_card_id=db_card.id,
            wallet_id=new_wallet.id,
            card=db_card  # Populate with the full card details
        )
        for db_card in valid_cards
    ]

    # Prepare the response as WalletSchema with CardInWalletSchema cards
    wallet_schema = WalletSchema(
        id=new_wallet.id,
        name=new_wallet.name,
        last_edited=new_wallet.last_edited,
        is_custom=new_wallet.is_custom,
        cards=card_in_wallet_schemas  # Now this list contains CardInWalletSchema instances
    )

    return wallet_schema

def edit_wallet(request: WalletUpdateRequest, db: Session, current_user):
    # Find the wallet by ID and ensure it belongs to the current user
    wallet = db.query(Wallet).filter_by(id=request.wallet_id, user_id=current_user.id).first()

    # If the wallet doesn't exist or isn't owned by the current user, raise an error
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found or access denied")

    # Update the wallet details if provided
    if request.name:
        wallet.name = request.name
    if request.is_custom is not None:
        wallet.is_custom = request.is_custom
    wallet.last_edited = datetime.today()

    # If cards are provided, update the wallet's card list
    if request.cards:
        # Clear existing cards
        wallet.cards = []
        
        # Add new cards by validating each one from the database
        for card in request.cards:
            db_card = db.query(CreditCard).filter_by(name=card.name, issuer=card.issuer).first()
            if not db_card:
                raise HTTPException(status_code=400, detail=f"Credit card {card.name} by {card.issuer} not found.")
            wallet.cards.append(db_card)

    # Commit changes to the database
    db.commit()
    db.refresh(wallet)

    return {"detail": "Wallet updated successfully"}

def delete_wallet(request: WalletDeleteRequest, db: Session, current_user: User):
    # Find the wallet by ID and ensure it belongs to the current user
    wallet = db.query(Wallet).filter_by(id=request.wallet_id, user_id=current_user.id).first()

    # If the wallet doesn't exist or isn't owned by the current user, raise an error
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found or access denied")

    # Delete the wallet
    db.delete(wallet)
    db.commit()

    return {"detail": "Wallet deleted successfully"}