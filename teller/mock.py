from creditcard.structure.openai.utils import structure_with_openai
from insights.schemas import HeavyHitterSchema, HeavyHittersResponse, VENDOR_CONST, CATEGORY_CONST
from database.teller.transactions import MockHeavyHitter
from insights.schemas import MonthlyTimeframe, CategorizationProgressSummary
from creditcard.enums import PurchaseCategory, RewardUnit, Vendors
from pydantic import BaseModel
from typing import Union, List, Optional
from sqlalchemy.orm import Session  
from datetime import date, timedelta

def heavy_hitters_prompt(user_bio):
    return f"""
    Based on a user's short plain text bio, estimate their likely monthly spending breakdown by categories and specific vendors. 
    Ensure each expense is counted only once, avoiding double-counting vendors within broader categories.

    Here is the users bio:

    {user_bio}
    """


def mock_heavy_hitters_response():
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "mock_heavy_hitters_response",
            "schema": {
                "type": "object",
                "properties": {
                    "mock_heavy_hitters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {                                
                                "name": {
                                    "type": "string",
                                    "enum": [purchase_category.value for purchase_category in PurchaseCategory] + [vendor.value for vendor in Vendors],
                                    "description": "The category or vendor associated with a purchase amount completed in a month"
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "Strictly positive number of dollars that were spent at the category or vendor."
                                },
                            },
                            "required": ["name", "amount"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["mock_heavy_hitters"],
                "additionalProperties": False
            },
            "strict": True
        }
    }

class MockHeavyHitter(BaseModel):
    amount: float
    name: Union[Vendors, PurchaseCategory]

class MockHeavyHittersResponse(BaseModel):
    mock_heavy_hitters: List[MockHeavyHitter]

def generate_and_save_heavy_hitters(user_bio: str, db: Session, user_id: Optional[int] = None, onboarding_id: Optional[int] = None) -> HeavyHittersResponse:
    print("generating and saving mocked heavy hitters")
    mock_response: MockHeavyHittersResponse = structure_with_openai(prompt=heavy_hitters_prompt(user_bio=user_bio), response_format=mock_heavy_hitters_response(), schema=MockHeavyHittersResponse)
    total = sum(map(lambda hh: hh.amount, mock_response.mock_heavy_hitters))
    
    if total == 0: 
        return HeavyHittersResponse(total=0, heavyhitters=[], timeframe=None, 
                                    categorization_progress_summary=CategorizationProgressSummary(), 
                                    )
    
    heavy_hitters = []

    for mock_heavy_hitter in mock_response.mock_heavy_hitters:
        type = None
        category = None
        if mock_heavy_hitter.name in Vendors:
            type = VENDOR_CONST
            category = Vendors.get_category(mock_heavy_hitter.name)
        elif mock_heavy_hitter.name in PurchaseCategory:
            type = CATEGORY_CONST
            category = mock_heavy_hitter.name

        heavy_hitter = HeavyHitterSchema(type=type, 
                        name=mock_heavy_hitter.name,
                        category=category,
                        percent=f"{round(mock_heavy_hitter.amount / (100 * total), 2)}%",
                        amount=mock_heavy_hitter.amount)
        heavy_hitter_db: MockHeavyHitter = heavy_hitter.to_db()
        
        if onboarding_id:
            heavy_hitter_db.onboarding_id = onboarding_id
        elif user_id:
            heavy_hitter_db.user_id = user_id
        else:
            raise ValueError("Either user_id or onboarding_id is required")
        
        db.add(heavy_hitter_db)
        db.commit()
        heavy_hitters.append(heavy_hitter)

    today = date.today()
    last_month = today - timedelta(days=32)
    return HeavyHittersResponse(total=total, heavyhitters=heavy_hitters, timeframe=MonthlyTimeframe(start_month=last_month, end_month=today), categorization_progress_summary=CategorizationProgressSummary(categorized_cc_eligible_count=1))


