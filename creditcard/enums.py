from enum import Enum

import re

def strip_up_to_period(text):
    parts = text.split('.', 1) 
    if len(parts) > 1:
        return parts[1].strip()
    return text.strip()

def single_nearest(text: str, enum : Enum):
    if text is None:
        return None
    
    for enum_element in enum:
        if strip_up_to_period(enum_element) in text:
            return enum_element
        
def multiple_nearest(text: str, enum : Enum):
    if text is None:
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
    PERCENT_CASHBACK_USD = "Percent Cashback USD",
    STATEMENT_CREDIT_USD = "Statement Credit USD",
    AVIOS = "Avios"
    AEROPLAN_POINTS = "Aeroplan Points"
    CHOICE_PRIVILEGES_POINTS = "Choice Privileges Points"
    UNKNOWN = "Unknown"
    
    @staticmethod
    def get_value(reward_unit) -> float:
        _values = {
            RewardUnit.CHASE_ULTIMATE_REWARDS: 0.0125, #  average from 1 to 1.5 cents.
            RewardUnit.AMEX_MEMBERSHIP_REWARDS: 0.006, # redeem for statement credits
            RewardUnit.CITI_THANKYOU_POINTS: 0.01, # 1 cent each when redeemed
            RewardUnit.CAPITAL_ONE_MILES: 0.005,  
            RewardUnit.WELLS_FARGO_GO_FAR_REWARDS: 0.01, 
            RewardUnit.BANK_OF_AMERICA_PREFERRED_REWARDS: 0.01,
            RewardUnit.BARCLAYS_ARRIVAL_POINTS: 0.01,
            RewardUnit.DISCOVER_CASHBACK_BONUS: 0.01,
            RewardUnit.US_BANK_ALTITUDE_POINTS: 0.0125, # 1.5 cents per point for travel, otherwise 1 cent per point
            RewardUnit.PNC_POINTS: 0.002, # 0.14 cents to 0.36. Best for travel.
            RewardUnit.HILTON_HONORS_POINTS: 0.006,
            RewardUnit.MARRIOTT_BONVOY_POINTS: 0.009,
            RewardUnit.WORLD_OF_HYATT_POINTS: 0.017,
            RewardUnit.DELTA_SKYMILES: 0.012,
            RewardUnit.UNITED_MILEAGEPLUS: 0.014, # average of 1.2 to 1.6 cents
            RewardUnit.AA_ADVANTAGE_MILES: 0.012, # when book flights 0.016
            RewardUnit.SOUTHWEST_RAPID_REWARDS: 0.014, # 1.3 cents to 1.5 cents.
            RewardUnit.IHG_ONE_REWARDS_POINTS: 0.006, 
            RewardUnit.JETBLUE_TRUEBLUE_POINTS: 0.0136,
            RewardUnit.ALASKA_MILEAGE_PLAN_MILES: 0.015, # from 1.2 cents to 1.8 cents. 
            RewardUnit.RADISSON_REWARDS_POINTS: 0.0045, # average of 0.4 cents to 0.5 cents 
            RewardUnit.PERCENT_CASHBACK_USD: 0.01,
            RewardUnit.AVIOS: 0.0135,
            RewardUnit.AEROPLAN_POINTS: 0.0145,
            RewardUnit.CHOICE_PRIVILEGES_POINTS: 0.008
        }
        return _values.get(reward_unit, 0.0)

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
    ACCOMMODATION = "accommodation"
    ADVERTISING = "advertising"
    BAR = "bar"
    CHARITY = "charity"
    CLOTHING = "clothing"
    DINING = "dining"
    EDUCATION = "education"
    ELECTRONICS = "electronics"
    ENTERTAINMENT = "entertainment"
    FUEL = "fuel"
    GENERAL = "general"
    GROCERIES = "groceries"
    HEALTH = "health"
    HOME = "home"
    INCOME = "income"
    INSURANCE = "insurance"
    INVESTMENT = "investment"
    LOAN = "loan"
    OFFICE = "office"
    PHONE = "phone"
    SERVICE = "service"
    SHOPPING = "shopping"
    SOFTWARE = "software"
    SPORT = "sport"
    TAX = "tax"
    TRANSPORT = "transport"
    TRANSPORTATION = "transportation"
    UTILITIES = "utilities"
    UNKNOWN = "unknown"

class IndustryType(str, Enum):
    OTHER = "Other"
    RESTAURANT = "Restaurant"
    HOTEL = "Hotel"
    HOTEL_RENTAL = "Hotel Rental"
    TECHNOLOGY = "Technology"
    HEALTHCARE = "Healthcare"
    ENTERTAINMENT = "Entertainment"
    CONSUMER_GOODS = "Consumer Goods"
    CONSTRUCTION = "Construction"

class BusinessSize(str, Enum):
    MICRO = "Micro (less than 10 employees)"
    SMALL = "Small (10-49 employees)"
    MEDIUM = "Medium (50-199 employees)"
    LARGE = "Large (200-499 employees)"
    ENTERPRISE = "Enterprise (500 or more employees)"

class Airline(str, Enum):
    AMERICAN_AIRLINES = "American Airlines"
    UNITED_AIRLINES = "United Airlines"
    ALASKAN_AIRLINES = "Alaskan Airlines"
    DELTA_AIRLINES = "Delta Airlines"
    JETBLUE_AIRLINES = "JetBlue Airlines"
    SOUTHWEST_AIRLINES = "Southwest Airlines"
    SKYWEST_AIRLINES = "SkyWest Airlines"
    ALASKA_AIRLINES = "Alaska Airlines"
    SPIRIT_AIRLINES = "Spirit Airlines"
    HAWAII_AIRLINES = "Hawaiian Airlines"

class Lifestyle(str, Enum):
    STUDENT = "Student"
    EARLY_CAREER = "Early Career"
    MID_CAREER = "Mid-Career"
    LATE_CAREER = "Late Career"
    RETIRED = "Retired"

class Vendors(str, Enum):
    AMAZON = "Amazon"
    TARGET = "Target"
    WALGREENS = "Walgreens"
    WALMART = "Walmart"
    KROGER = "Kroger"
    LOWES = "Lowes"
    ALDI = "Aldi"
    COSTCO = "Costco"
    UNKNOWN = "Unknown"

    def get_category(vendor) -> PurchaseCategory:
        _values = {
            Vendors.AMAZON: PurchaseCategory.SHOPPING,
            Vendors.TARGET: PurchaseCategory.SHOPPING,
            Vendors.WALGREENS: PurchaseCategory.GROCERIES,
            Vendors.WALMART: PurchaseCategory.GROCERIES,
            Vendors.KROGER: PurchaseCategory.GROCERIES,
            Vendors.LOWES: PurchaseCategory.GROCERIES,
            Vendors.ALDI: PurchaseCategory.GROCERIES,
            Vendors.COSTCO: PurchaseCategory.GROCERIES,
        }

        return _values.get(vendor, PurchaseCategory.GENERAL)
    
    def get_vendor(name: str, description: str):
        def check_string_for_vendor_name(s: str):
            if s:
                for vendor in Vendors:
                    if re.search(rf'\b{vendor.value}\b', s, re.IGNORECASE):
                        return vendor
            return None

        # First check in name
        out = check_string_for_vendor_name(name)
        
        # If not found in name, check the full description
        if out is None:
            out = check_string_for_vendor_name(description)

        # Return found vendor or UNKNOWN if no vendor is found
        return out if out else Vendors.UNKNOWN

class APRType(str, Enum):
    PURCHASE = "Purchase"
    CASH_ADVANCE = "Cash Advance"
    BALANCE_TRANSFER = "Balance Transfer"
    PROMOTIONAL = "Promotional"
    PENALTY = "Penalty"