from creditcard.schemas import CreditCardSchema, CreditCardsFilter
from creditcard.enums import CreditNeeded, Lifestyle, CreditCardKeyword
from creditcard.schemas import CreditCardsDatabaseRequest, CreditCardsDatabaseResponse
from teller.schemas import PreferencesSchema
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

    query = db.query(CreditCard)

    if request.use_preferences and current_user:
        preferences: PreferencesSchema = current_user.preferences
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

            # Filter by credit score
            if credit_score:
                credit_scores = CreditNeeded.get_from_user_credit(credit_score)
                query = query.filter(
                    CreditCard.credit_needed.op('->>')('key').in_(credit_scores)
                )

            # Apply bank preferences
            if preferred_banks:
                query = query.filter(CreditCard.issuer.in_(preferred_banks))
            if have_banks:
                query = query.filter(CreditCard.issuer.in_(have_banks))
            if avoid_banks:
                query = query.filter(~CreditCard.issuer.in_(avoid_banks))

            # Apply rewards program preferences
            if preferred_rewards_programs:
                query = query.filter(CreditCard.primary_reward_unit.in_(preferred_rewards_programs))
            if avoid_rewards_programs:
                query = query.filter(~CreditCard.primary_reward_unit.in_(avoid_rewards_programs))

            # Exclude unwanted keywords
            business_keywords = [
                    CreditCardKeyword.business.value,
                    CreditCardKeyword.small_business.value
                ]
            wanted_keywords = request.card_details.keywords if isinstance(request.card_details, CreditCardsFilter) else None
            if not preferences.business_preferences and wanted_keywords and set(business_keywords).isdisjoint(wanted_keywords):
                query = query.filter(
                    ~CreditCard.keywords.op('->>')('key').in_(business_keywords))
            if wanted_keywords:
                query = query.filter(
                    CreditCard.keywords.op('->>')('key').in_(wanted_keywords))

    elif request.card_details and request.card_details == "all":
        credit_cards = query.limit(request.max_num).all()
        return CreditCardsDatabaseResponse(
            credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards]
        )

    credit_cards = query.limit(request.max_num).all()
    return CreditCardsDatabaseResponse(
        credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards]
    )
