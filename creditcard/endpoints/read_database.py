from creditcard.endpoints.schemas import CreditCardsDatabaseRequest, CreditCardsFilter
from creditcard.enums import CreditNeeded, CreditCardKeyword
from creditcard.schemas import CreditCardSchema
from database.auth.user import User
from database.creditcard.creditcard import CreditCard
from database.teller.preferences import Preferences
from pydantic import BaseModel
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import JSONB, array
from sqlalchemy.orm import Session
from teller.schemas import PreferencesSchema
from typing import List, Optional
import logging

class CreditCardsDatabaseResponse(BaseModel):
    credit_card: List[CreditCardSchema]

async def read_credit_cards_database(
    request: CreditCardsDatabaseRequest,
    db: Session,
    current_user: Optional[User] = None
) -> CreditCardsDatabaseResponse:
    if request.max_num is None:
        request.max_num = 1000

    query = db.query(CreditCard)

    if request.use_preferences and current_user:
        preferences: PreferencesSchema = PreferencesSchema()
        if isinstance(current_user, User): 
            preferences: PreferencesSchema = current_user.preferences
            if not preferences:
                logging.info("Additional database query to retrieve the user's preferences")
                query_preferences = db.query(Preferences).filter(Preferences.user_id == current_user.id).first()
                if query_preferences:
                    preferences = PreferencesSchema.model_validate(query_preferences, exclude_unset=True)
                else:
                    preferences = PreferencesSchema()
                    logging.info("No preferences found for the user. Using empty preferences.")

            logging.info(f"Using preferences: {preferences}")

        if preferences:
            credit_profile_preferences = preferences.credit_profile
            credit_score = credit_profile_preferences.credit_score if credit_profile_preferences else None

            banks_preferences = preferences.banks_preferences
            have_banks = banks_preferences.have_banks if banks_preferences else None
            preferred_banks = banks_preferences.preferred_banks if banks_preferences else None
            avoid_banks = banks_preferences.avoid_banks if banks_preferences else None

            rewards_preferences = preferences.rewards_programs_preferences
            preferred_rewards_programs = rewards_preferences.preferred_rewards_programs if rewards_preferences else None
            avoid_rewards_programs = rewards_preferences.avoid_rewards_programs if rewards_preferences else None

            if credit_score:
                credit_scores = CreditNeeded.get_from_user_credit(credit_score)
                query = query.filter(
                    cast(CreditCard.credit_needed, JSONB).has_any(array(credit_scores))
                )


            if preferred_banks:
                query = query.filter(CreditCard.issuer.in_(array(preferred_banks)))
            if have_banks:
                query = query.filter(CreditCard.issuer.in_(array(have_banks)))
            if avoid_banks:
                query = query.filter(~CreditCard.issuer.in_(array(avoid_banks)))

            if preferred_rewards_programs:
                query = query.filter(CreditCard.primary_reward_unit.in_(preferred_rewards_programs))
            if avoid_rewards_programs:
                query = query.filter(~CreditCard.primary_reward_unit.in_(avoid_rewards_programs))

            wanted_keywords = request.card_details.keywords if isinstance(request.card_details, CreditCardsFilter) and request.card_details.keywords else []

            business_keywords = [
                CreditCardKeyword.business.value,
                CreditCardKeyword.small_business.value
            ]
            
            if set(business_keywords).isdisjoint(wanted_keywords):
                logging.info("Including rows that do NOT match business keywords")
                query = query.filter(
                    ~(cast(CreditCard.keywords, JSONB).has_any(array(business_keywords)))
                )
            else :
                logging.info("Including business keywords")

    credit_cards = query.limit(request.max_num).all()
    return CreditCardsDatabaseResponse(credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards])
