from creditcard.schemas import CreditCardSchema
from creditcard.schemas import CreditCardsDatabaseRequest, CreditCardsDatabaseResponse
from database.creditcard.creditcard import CreditCard
from sqlalchemy.orm import Session
from database.auth.user import User
from typing import Optional

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
            # Get banks preferences with null safety
            banks_preferences = preferences.banks_preferences
            have_banks = banks_preferences.have_banks if banks_preferences and banks_preferences.have_banks else []
            preferred_banks = banks_preferences.preferred_banks if banks_preferences and banks_preferences.preferred_banks else []
            avoid_banks = banks_preferences.avoid_banks if banks_preferences and banks_preferences.avoid_banks else []

            # Get rewards programs preferences with null safety
            rewards_preferences = preferences.rewards_programs_preferences
            preferred_rewards_programs = rewards_preferences.preferred_rewards_programs if rewards_preferences and rewards_preferences.preferred_rewards_programs else []
            avoid_rewards_programs = rewards_preferences.avoid_rewards_programs if rewards_preferences and rewards_preferences.avoid_rewards_programs else []

            # Build the query with null-safe filters
            query = db.query(CreditCard)

            # Apply banks preferences filters
            if preferred_banks:
                query = query.filter(CreditCard.issuer.in_(preferred_banks))
            if have_banks:
                query = query.filter(CreditCard.issuer.in_(have_banks))
            if avoid_banks:
                query = query.filter(~CreditCard.issuer.in_(avoid_banks))

            # # Apply rewards programs preferences filters
            # if preferred_rewards_programs:
            #     query = query.filter(CreditCard.rewards_programs.overlap(preferred_rewards_programs))
            # if avoid_rewards_programs:
            #     query = query.filter(~CreditCard.rewards_programs.overlap(avoid_rewards_programs))

            # You can also add filters based on other preferences if needed
            # For example, apply consumer preferences or credit profile preferences

            credit_cards = query.limit(request.max_num).all()
            return CreditCardsDatabaseResponse(
                credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards]
            )
        else:
            # Handle the case where preferences are None
            credit_cards = db.query(CreditCard).limit(request.max_num).all()
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

        if request.card_details.benefits:
            query = query.filter(CreditCard.benefits.overlap(request.card_details.benefits))
        if request.card_details.issuer:
            query = query.filter(CreditCard.issuer == request.card_details.issuer)
        if request.card_details.credit_needed:
            query = query.filter(CreditCard.credit_needed.in_(request.card_details.credit_needed))
        if request.card_details.apr is not None:
            query = query.filter(CreditCard.apr < request.card_details.apr)

        credit_cards = query.limit(request.max_num).all()
        return CreditCardsDatabaseResponse(
            credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards]
        )
