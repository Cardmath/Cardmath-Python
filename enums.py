from enum import Enum

def strip_up_to_period(text):
    parts = text.split('.', 1) 
    if len(parts) > 1:
        return parts[1].strip()
    return text.strip()

def single_nearest(text: str, enum : Enum):
    if (text == None):
        return None
    
    for enum_element in enum:
        if strip_up_to_period(enum_element) in text:
            return enum_element
        
def multiple_nearest(text: str, enum : Enum):
    if (text == None):
        return None
    
    out_enums = []
    for enum_element in enum:
        if strip_up_to_period(enum_element) in text:
            out_enums.append(enum_element)
    return out_enums

class Issuer(str, Enum):
    CAPITAL_ONE = "Capital One"
    CHASE = "Chase"
    AMERICAN_EXPRESS = "American Express"
    CITI = "Citi"
    DISCOVER = "Discover"
    BANK_OF_AMERICA = "Bank of America"
    WELLS_FARGO = "Wells Fargo"
    BARCLAYS = "Barclays"
    US_BANK = "US Bank"
    PNC = "PNC"
    TD_BANK = "TD Bank"
    HSBC = "HSBC"
    
class RewardUnit(str, Enum):
    CHASE_ULTIMATE_REWARDS = "Chase Ultimate Rewards"
    AMEX_MEMBERSHIP_REWARDS = "American Express Membership Rewards"
    CITI_THANKYOU_POINTS = "Citi ThankYou Points"
    CAPITAL_ONE_MILES = "Capital One Miles"
    WELLS_FARGO_GO_FAR_REWARDS = "Wells Fargo Go Far Rewards"
    BANK_OF_AMERICA_PREFERRED_REWARDS = "Bank of America Preferred Rewards"
    BARCLAYS_ARRIVAL_POINTS = "Barclays Arrival Points"
    DISCOVER_CASHBACK_BONUS = "Discover Cashback Bonus"
    US_BANK_ALTITUDE_POINTS = "U.S. Bank Altitude Points"
    PNC_POINTS = "PNC Points"
    HILTON_HONORS_POINTS = "Hilton Honors Points"
    MARRIOTT_BONVOY_POINTS = "Marriott Bonvoy Points"
    WORLD_OF_HYATT_POINTS = "World of Hyatt Points"
    DELTA_SKYMILES = "Delta SkyMiles"
    UNITED_MILEAGEPLUS = "United MileagePlus"
    AA_ADVANTAGE_MILES = "American Airlines AAdvantage Miles"
    SOUTHWEST_RAPID_REWARDS = "Southwest Rapid Rewards"
    IHG_ONE_REWARDS_POINTS = "IHG One Rewards Points"
    JETBLUE_TRUEBLUE_POINTS = "JetBlue TrueBlue Points"
    ALASKA_MILEAGE_PLAN_MILES = "Alaska Mileage Plan Miles"
    RADISSON_REWARDS_POINTS = "Radisson Rewards Points"
    

# Define an enum for benefits
class Benefit(str, Enum):
    AIRPORT_LOUNGE_ACCESS = "airport lounge access"
    CELL_PHONE_PROTECTION = "cell phone protection"
    CONCIERGE_SERVICE = "concierge service"
    EMERGENCY_MEDICAL_INSURANCE = "emergency medical insurance"
    EVENT_TICKET_ACCESS = "event ticket access"
    EXTENDED_RETURN_PERIOD = "extended return period"
    EXTENDED_WARRANTY = "extended warranty"
    FREE_CHECKED_BAGS = "free checked bags"
    GLOBAL_ENTRY_TSA_PRECHECK_CREDIT = "global entry/tsa precheck credit"
    NO_FOREIGN_TRANSACTION_FEES = "no foreign transaction fees"
    PRICE_PROTECTION = "price protection"
    PRIORITY_BOARDING = "priority boarding"
    PURCHASE_PROTECTION = "purchase protection"
    RENTAL_CAR_INSURANCE = "rental car insurance"
    RETURN_PROTECTION = "return protection"
    TRAVEL_ASSISTANCE_SERVICES = "travel assistance services"
    TRAVEL_INSURANCE = "travel insurance"
    
    
# Define an enum for credit needed
class CreditNeeded(str, Enum):
    EXCELLENT = "Excellent" # 720-850
    GOOD = "Good" # 690-719
    FAIR = "Fair" # 630-689
    POOR = "Bad" # 0-629 
    
class PurchaseCategory(str, Enum):
    TRAVEL = "Travel"
    DINING = "Dining"
    GROCERIES = "Groceries"
    GAS_AND_TRANSPORTATION = "Gas and Transportation"
    ENTERTAINMENT = "Entertainment"
    RETAIL_SHOPPING = "Retail Shopping"
    UTILITIES_AND_SERVICES = "Utilities and Services"
    HEALTH_AND_WELLNESS = "Health and Wellness"
    ELECTRONICS_AND_TECHNOLOGY = "Electronics and Technology"
    CHARITABLE_DONATIONS = "Charitable Donations"
    ONLINE_SHOPPING = "Online Shopping"