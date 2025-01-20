import requests
from creditcard.enums import CardKey
from database.creditcard.source import UpdateableSourceColumns

BASE_URL = 'rewards-credit-card-api.p.rapidapi.com'
BY_CARD = 'creditcard-detail-bycard'
HEADERS = {
    'x-rapidapi-host': 'rewards-credit-card-api.p.rapidapi.com',
    'x-rapidapi-key' : 'fb0e3bff1bmsh0fdea00850b4ac3p113d0cjsn0a80309fb977'
}


def get_card(cardKey: CardKey) -> dict:
    r = requests.get(url=f"{BASE_URL}/{BY_CARD}/{cardKey}", headers=HEADERS).json()

def get_extractor(col: UpdateableSourceColumns) -> callable:
    map = {
        UpdateableSourceColumns.ANNUAL_FEE: extract_annual_fee,
        UpdateableSourceColumns.BENEFITS: extract_benefits,
        UpdateableSourceColumns.CREDIT_NEEDED: extract_credit_needed,
        UpdateableSourceColumns.STATEMENT_CREDIT: extract_statement_credit,
        UpdateableSourceColumns.SIGN_ON_BONUS: extract_sign_on_bonus,
        UpdateableSourceColumns.REWARD_CATEGORY_MAP: extract_reward_category_map
    }
    
    return map.get(col)

def extract_credit_needed(rewardscc_response: dict):
    return {
        "Credit required:" : rewardscc_response.get('creditRange') 
    }

def extract_annual_fee(rewardscc_response: dict):
    return {
        "First year annual fee" : rewardscc_response.get('signupAnnualFee'),
        "Is annual fee waived first year? (0=no, 1=yes)" : rewardscc_response.get('isSignupAnnualFeeWaived'),
        "Annual fee in USD": rewardscc_response.get('annualFee')
    }

def extract_benefits(rewardscc_response: dict):
    benefits_list = []
    
    for benefit in rewardscc_response.get('benefit', []):
        benefit_info = {
            "title": benefit.get('benefitTitle'),
            "description": benefit.get('benefitDesc')
        }
        benefits_list.append(benefit_info)
    
    return {
        "Benefits": benefits_list,
        "Does card include lounge access? (0=no, 1=yes)": rewardscc_response.get('isLoungeAccess'),
        "Lounge access benefit description": rewardscc_response.get('loungeAccess'),
        "Free annual hotel night certificate description": rewardscc_response.get('freeHotelNight'),
        "Does card include a free checked bag? (0=no, 1=yes)": rewardscc_response.get('isFreeCheckedBag'),
        "Free airline checked bag description": rewardscc_response.get('freeCheckedBag'),
    }

def extract_statement_credit(rewardscc_response: dict):
    return {
        "Does card have trusted traveler credit? (0=no, 1=yes)": rewardscc_response.get('isTrustedTraveler'),
        "Trusted traveler credit description": rewardscc_response.get('trustedTraveler')
        ### Fill in
    }

def extract_sign_on_bonus(rewardscc_response: dict):
    return {
        "Has sign-up bonus? (0=no, 1=yes)": rewardscc_response.get('isSignupBonus'),
        "Sign-up bonus amount": rewardscc_response.get('signupBonusAmount'),
        "Redemption program": rewardscc_response.get('signupBonusType'),
        "Sign-up bonus category": rewardscc_response.get('signupBonusCategory'),
        "Sign-up bonus item": rewardscc_response.get('signupBonusItem'),
        "Minimum spend required": rewardscc_response.get('signupBonusSpend'),
        "Time period length": rewardscc_response.get('signupBonusLength'),
        "Time period unit": rewardscc_response.get('signupBonusLengthPeriod'),
        "Sign-up bonus description": rewardscc_response.get('signupBonusDesc'),
        "Additional statement credit": rewardscc_response.get('signupStatementCredit')
    }

def extract_reward_category_map(rewardscc_response: dict):
    reward_categories = []
    
    # Base earn rate
    base_earn = {
        "category": "Base",
        "points_per_dollar": rewardscc_response.get('baseSpendAmount'),
        "reward_program": rewardscc_response.get('baseSpendEarnType'),
        "category_type": "Base"
    }
    reward_categories.append(base_earn)
    
    # Bonus categories
    bonus_categories = rewardscc_response.get('spendBonusCategory', [])
    for category in bonus_categories:
        bonus_earn = {
            "category": category.get('spendBonusCategoryName'),
            "category_type": category.get('spendBonusCategoryType'),
            "category_group": category.get('spendBonusCategoryGroup'),
            "subcategory": category.get('spendBonusSubcategoryGroup'),
            "points_per_dollar": category.get('earnMultiplier'),
            "description": category.get('spendBonusDesc'),
            "has_spend_limit": category.get('isSpendLimit'),
            "spend_limit": category.get('spendLimit'),
            "spend_limit_reset": category.get('spendLimitResetPeriod'),
            "has_date_limit": category.get('isDateLimit'),
            "valid_from": category.get('limitBeginDate'),
            "valid_to": category.get('limitEndDate')
        }
        reward_categories.append(bonus_earn)
    
    return {
        "reward_categories": reward_categories,
        "annual_spend_bonus_description": rewardscc_response.get('annualSpendDesc')
    }