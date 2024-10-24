from creditcard.schemas import CreditCardSchema
from creditcard.schemas import CreditCardsDatabaseRequest, CreditCardsDatabaseResponse
from database.creditcard.creditcard import CreditCard
from sqlalchemy.orm import Session

async def read_credit_cards_database(request: CreditCardsDatabaseRequest, db: Session) -> CreditCardsDatabaseResponse:
    if request.max_num is None:
        request.max_num = 100
        
    if request.card_details and request.card_details == "all":
        credit_cards = db.query(CreditCard).limit(request.max_num).all()
        return CreditCardsDatabaseResponse(credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards])
    
    credit_cards = db.query(CreditCard).filter(
        CreditCard.benefits.overlap(request.card_details.benefits or []) != [],
        (request.card_details.issuer is None or CreditCard.issuer == request.card_details.issuer),
        CreditCard.credit_needed.in_(request.card_details.credit_needed or []),
        (request.card_details.apr is None or CreditCard.apr < request.card_details.apr)
    ).limit(request.max_num).all()
    print(credit_cards)
    return CreditCardsDatabaseResponse(credit_card=[CreditCardSchema.model_validate(cc) for cc in credit_cards])