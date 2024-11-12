from creditcard.schemas import CreditCardSchema
from creditcard.enums import CreditNeeded, Lifestyle, CreditCardKeyword
from creditcard.schemas import CreditCardsDatabaseRequest, CreditCardsDatabaseResponse
from database.creditcard.creditcard import CreditCard
from sqlalchemy.orm import Session
from sqlalchemy import Float, or_, and_
from sqlalchemy.dialects.postgresql import JSONB, array
from database.auth.user import User
from typing import Optional, List

async def read_credit_cards_database(
    request: CreditCardsDatabaseRequest,
    db: Session,
    current_user: Optional[User] = None
) -> CreditCardsDatabaseResponse:
    if request.max_num is None:
        request.max_num = 1000

    if request.use_preferences and current_user:
        preferences = current_user.preferences

        if preferences:
            credit_profile_preferences = preferences.credit_profile
            credit_score = credit_profile_preferences.credit_score if credit_profile_preferences else -1
            lifestyle = credit_profile_preferences.lifestyle if credit_profile_preferences else None

            banks_preferences = preferences.banks_preferences
            have_banks = banks_preferences.have_banks if banks_preferences else []
            preferred_banks = banks_preferences.preferred_banks if banks_preferences else []
            avoid_banks = banks_preferences.avoid_banks if banks_preferences else []

            rewards_preferences = preferences.rewards_programs_preferences
            preferred_rewards_programs = rewards_preferences.preferred_rewards_programs if rewards_preferences else []
            avoid_rewards_programs = rewards_preferences.avoid_rewards_programs if rewards_preferences else []

            consumer_preferences = preferences.consumer_preferences
            favorite_grocery_stores = consumer_preferences.favorite_restaurants if consumer_preferences else []
            favorite_general_goods_stores = consumer_preferences.favorite_general_goods_stores if consumer_preferences else []

            business_preferences = preferences.business_preferences
            business_type = business_preferences.business_type if business_preferences else []
            business_size = business_preferences.business_size if business_preferences else []

            query = db.query(CreditCard)

            # Filter by credit score if available
            if credit_score and credit_score > 0:
                credit_scores: List[CreditNeeded] = CreditNeeded.get_from_user_credit(credit_score)
                query = query.filter(CreditCard.credit_needed.contains(credit_scores))

            if lifestyle and lifestyle == Lifestyle.STUDENT:
                query = query.filter(CreditCard.keywords.contains([CreditCardKeyword.student.value]))

            # Apply banks preferences filters
            if preferred_banks:
                query = query.filter(CreditCard.issuer.in_(preferred_banks))
            if have_banks:
                query = query.filter(CreditCard.issuer.in_(have_banks))
            if avoid_banks:
                query = query.filter(~CreditCard.issuer.in_(avoid_banks))

            # Apply rewards programs preferences filters
            if preferred_rewards_programs:
                query = query.filter(CreditCard.primary_reward_unit.in_(preferred_rewards_programs))
            if avoid_rewards_programs:
                query = query.filter(~CreditCard.primary_reward_unit.in_(avoid_rewards_programs))

            # Exclude cards based on unwanted keywords
            unwanted_keywords = []
            if not (business_type or business_size):
                # User does not want business cards
                unwanted_keywords.extend([
                    CreditCardKeyword.business.value,
                    CreditCardKeyword.small_business.value
                ])

            if unwanted_keywords:
                # Exclude records where any unwanted keyword is present
                query = query.filter(
                    ~CreditCard.keywords.cast(JSONB).has_any(array(unwanted_keywords))
                )

            # Additional filters can be applied here if needed

            credit_cards = query.limit(request.max_num).all()
            print(f"[INFO] Number of credit cards: {len(credit_cards)}")
            return CreditCardsDatabaseResponse(
                credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards]
            )
        else:
            # Handle the case where preferences are None
            unwanted_keywords = [
                CreditCardKeyword.business.value,
                CreditCardKeyword.small_business.value,
                CreditCardKeyword.customizable_rewards.value
            ]

            query = db.query(CreditCard).filter(
                ~CreditCard.keywords.cast(JSONB).has_any(array(unwanted_keywords))
            )

            credit_cards = query.limit(request.max_num).all()
            return CreditCardsDatabaseResponse(
                credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards]
            )

    elif request.card_details and request.card_details == "all":
        credit_cards = db.query(CreditCard).limit(request.max_num).all()
        return CreditCardsDatabaseResponse(
            credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards]
        )
    else:
        query = db.query(CreditCard)

        # Individual filters for card details
        if request.card_details.benefits:
            query = query.filter(CreditCard.benefits.overlap(request.card_details.benefits))
        if request.card_details.issuer:
            query = query.filter(CreditCard.issuer == request.card_details.issuer)
        if request.card_details.credit_needed:
            query = query.filter(CreditCard.credit_needed.contains(request.card_details.credit_needed))
        if request.card_details.apr is not None:
            query = query.filter(CreditCard.apr[0].astext.cast(Float) < request.card_details.apr)

        credit_cards = query.limit(request.max_num).all()
        return CreditCardsDatabaseResponse(
            credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards]
        )
