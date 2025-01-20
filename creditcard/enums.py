from enum import Enum
from typing import List

import re

class Network(str, Enum):
    VISA = "Visa"
    MASTERCARD = "MasterCard"
    AMERICAN_EXPRESS = "American Express"
    DISCOVER = "Discover"

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
    
    
class CreditNeeded(str, Enum):
    EXCELLENT = "Excellent" # 720-850
    GOOD = "Good" # 690-719
    FAIR = "Fair" # 630-689
    POOR = "Bad" # 0-629 

    @staticmethod
    def get_value(credit_needed) -> float:
        _values = {
            CreditNeeded.EXCELLENT: 850,
            CreditNeeded.GOOD: 719,
            CreditNeeded.FAIR: 689,
            CreditNeeded.POOR: 629
        }
        return _values.get(credit_needed, 0.0)
    
    @classmethod
    def get_from_user_credit(cls, user_credit) -> List[str]:
        _values = [
            (CreditNeeded.EXCELLENT, (720, 850)),
            (CreditNeeded.GOOD, (690, 719)),
            (CreditNeeded.FAIR, (630, 689)),
            (CreditNeeded.POOR, (0, 629))
        ]
        result = []
        for credit_needed, (lower, upper) in _values:
            if user_credit <= upper:
                result.append(credit_needed)
        return result
    
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

        out = check_string_for_vendor_name(name)
        
        if out is None:
            out = check_string_for_vendor_name(description)

        return out if out else Vendors.UNKNOWN
    

    @staticmethod
    def get_category(vendor):
        grocery_vendors = {Vendors.WALGREENS, Vendors.WALMART, Vendors.KROGER, Vendors.LOWES, Vendors.ALDI, Vendors.COSTCO}
        shopping_vendors = {Vendors.AMAZON, Vendors.TARGET}
        if vendor in grocery_vendors:
            return PurchaseCategory.GROCERIES
        elif vendor in shopping_vendors:
            return PurchaseCategory.SHOPPING
        else:
            return None

class APRType(str, Enum):
    PURCHASE = "Purchase"
    CASH_ADVANCE = "Cash Advance"
    BALANCE_TRANSFER = "Balance Transfer"
    PROMOTIONAL = "Promotional"
    PENALTY = "Penalty"

class CreditCardKeyword(str, Enum):
    business = "Business"
    personal = "Personal"
    student = "Student"
    travel = "Travel"
    rewards_focused = "Rewards-focused"
    customizable_rewards = "Customizable Rewards"
    low_apr = "Low APR"
    no_annual_fee = "No Annual Fee"
    cashback = "Cashback"
    balance_transfer = "Balance Transfer"
    secured = "Secured"
    high_limit = "High Limit"
    luxury = "Luxury"
    airline = "Airline"
    hotel = "Hotel"
    gas = "Gas"
    grocery = "Grocery"
    dining = "Dining"
    small_business = "Small Business"
    intro_apr = "Intro APR"

class CardAction(str, Enum):
    keep = "Keep this card"
    cancel = "Cancel this card"
    add = "Add this card"

class CardKey(str, Enum):
    WELLSFARGO_NOT_FOUND = "wellsfargo-not-found"
    USBANK_LATAMSECURED = "usbank-latamsecured"
    USBANK_LATAMVISA = "usbank-latamvisa"
    CHASE_MARRIOTTBOLD = "chase-marriottbold"
    CHASE_AMAZONPRIME = "chase-amazonprime"
    CITI_PREMIERPASSEXPEDIA = "citi-premierpassexpedia"
    USBANK_RADISSONPREMIER = "usbank-radissonpremier"
    CITI_SIMPLICITYCASH = "citi-simplicitycash"
    USBANK_POLARIS = "usbank-polaris"
    PNC_BIZ_VISABUSINESS = "pnc-biz-visabusiness"
    BARCLAYS_MASTERCARDBLACK = "barclays-mastercardblack"
    CAPITALONE_BIZ_SPARKCLASSIC = "capitalone-biz-sparkclassic"
    PNC_PREMIERTRAVELERVISA = "pnc-premiertravelervisa"
    CITI_REWARDSPLUSSTUDENT = "citi-rewardsplusstudent"
    BOA_SUSANKOMEN = "boa-susankomen"
    DISCOVER_STUDENTCHROME = "discover-studentchrome"
    CITI_PREMIERPASSEXPEDIAELITE = "citi-premierpassexpediaelite"
    DISCOVER_CASHBACK = "discover-cashback"
    BOA_TRAVELREWARDSSTUDENTS = "boa-travelrewardsstudents"
    BARCLAYS_BREEZE = "barclays-breeze"
    BOA_ALLEGIANT = "boa-allegiant"
    BOA_CELECRITYCRUISES = "boa-celecritycruises"  # (Note potential typo in original)
    CHASE_INKPREMIER = "chase-inkpremier"
    CAPITALONE_QUICKSILVERSTUDENTS = "capitalone-quicksilverstudents"
    AMEX_MORGANSTANLEYPLATINUM = "amex-morganstanleyplatinum"
    USBANK_CASHREWARDSVISA = "usbank-cashrewardsvisa"
    CHASE_MARRIOTTBONVOYPREMIER = "chase-marriottbonvoypremier"
    USBANK_BIZ_ALTITUDECONNECT = "usbank-biz-altitudeconnect"
    CITI_BIZ_COSTCOANYWHEREVISA = "citi-biz-costcoanywherevisa"
    CHASE_IBERIA = "chase-iberia"
    CAPITALONE_QUICKSILVERSECURED = "capitalone-quicksilversecured"
    CITI_RADIOSHACK = "citi-radioshack"
    BARCLAYS_UBERVISA = "barclays-ubervisa"
    USBANK_STARTFARMPREMIER = "usbank-startfarmpremier"
    USBANK_BIZ_RADISSON = "usbank-biz-radisson"
    USBANK_LATAMVISASIGNATURE = "usbank-latamvisasignature"
    BOA_AAAVISASIGNATURE = "boa-aaavisasignature"
    BOA_ELITEVISA = "boa-elitevisa"
    WELLSFARGO_ADVISORS = "wellsfargo-advisors"
    CHASE_MARRIOTTBONVOYVISASIGNATURE = "chase-marriottbonvoyvisasignature"
    CITI_TSC = "citi-tsc"
    USBANK_INFINITE = "usbank-infinite"
    PNC_BIZ_BUSINESSOPTIONSVISA = "pnc-biz-businessoptionsvisa"
    BARCLAYS_PRINCESSCRUISES = "barclays-princesscruises"
    USBANK_BIZ_LEVERAGE = "usbank-biz-leverage"
    CHASE_MARRIOTTBOUNDLESS = "chase-marriottboundless"
    CITI_SECUREDMASTERCARD = "citi-securedmastercard"
    CAPITALONE_PLATINUMSECURED = "capitalone-platinumsecured"
    TDBANK_CASHSECURED = "tdbank-cashsecured"
    USBANK_SMARTLY = "usbank-smartly"
    BARCLAYS_FRONTIER = "barclays-frontier"
    CAPITALONE_WESTELM = "capitalone-westelm"
    DISCOVER_STUDENTCASHBACK = "discover-studentcashback"
    AMEX_MARRIOTBONVOYAMEX = "amex-marriotbonvoyamex"
    BOA_AMERICARDSTUDENT = "boa-americardstudent"
    AMEX_HILTONSURPASS = "amex-hiltonsurpass"
    BOA_CUSTOMIZEDCASHREWARDS = "boa-customizedcashrewards"
    BOA_NYUAACUSTOMIZEDCASH = "boa-nyuaacustomizedcash"
    AMEX_BIZ_CORPORATEPLATINUM = "amex-biz-corporateplatinum"
    PNC_COREVISA = "pnc-corevisa"
    CAPITALONE_SAVORONESTUDENTS = "capitalone-savoronestudents"
    BARCLAYS_EMIRATESSKYWARDSPREMIUM = "barclays-emiratesskywardspremium"
    USBANK_SHOPPERCASHREWARDS = "usbank-shoppercashrewards"
    USBANK_SECUREDVISA = "usbank-securedvisa"
    USBANK_ALTITUDECONNECT = "usbank-altitudeconnect"
    BARCLAYS_HOLLANDAMERICA = "barclays-hollandamerica"
    AMEX_HILTON = "amex-hilton"
    AMEX_HILTONASPIRE = "amex-hiltonaspire"
    USBANK_CASHPLUSSECUREDVISA = "usbank-cashplussecuredvisa"
    DISCOVER_SECURED = "discover-secured"
    HSBC_PREMIER = "hsbc-premier"
    AMEX_BIZ_MARRIOTTBONVOY = "amex-biz-marriottbonvoy"
    PNC_CASHREWARDSVISA = "pnc-cashrewardsvisa"
    BOA_ALASKA = "boa-alaska"
    USBANK_STATEFARMGOODNEIGHBOR = "usbank-statefarmgoodneighbor"
    CAPITALONE_POTTERYBARN = "capitalone-potterybarn"
    AMEX_MARRIOTTBONVOYBRILLIANT = "amex-marriottbonvoybrilliant"
    USBANK_BIZ_TRIPLECASH = "usbank-biz-triplecash"
    CHASE_IHGREWARDSCLASSIC = "chase-ihgrewardsclassic"
    BOA_AMERICARDSECURED = "boa-americardsecured"
    USBANK_PLATINUM = "usbank-platinum"
    BOA_USPRIDECUSTOMIZED = "boa-uspridecustomized"
    BOA_ABAVISA = "boa-abavisa"
    WELLSFARGO_MICROCENTER = "wellsfargo-microcenter"
    WELLSFARGO_CASHWISE = "wellsfargo-cashwise"
    CHASE_SOUTHWESTPREMIER = "chase-southwestpremier"
    CITI_PREMIER = "citi-premier"
    BOA_ROYALCARRIBEAN = "boa-royalcarribean"
    USBANK_RADISSONVISA = "usbank-radissonvisa"
    BOA_ASIANA = "boa-asiana"
    CHASE_SAPPHIRE = "chase-sapphire"
    BARCLAYS_EMIRATESSKYWARDS = "barclays-emiratesskywards"
    CHASE_FREEDOMSTUDENT = "chase-freedomstudent"
    WELLSFARGO_BIZ_SECURED = "wellsfargo-biz-secured"
    USBANK_SKYPASSSELECT = "usbank-skypassselect"
    USBANK_COLLEGEVISA = "usbank-collegevisa"
    CITI_BESTBUY = "citi-bestbuy"
    USBANK_PERKSPLUSVISA = "usbank-perksplusvisa"
    TDBANK_FIRSTCLASS = "tdbank-firstclass"
    BARCLAYS_VISAAPPLEREWARDS = "barclays-visaapplerewards"
    WELLSFARGO_SECURED = "wellsfargo-secured"
    CHASE_UNITEDMILEAGEPLUSVISA = "chase-unitedmileageplusvisa"
    CHASE_JPMORGANRESERVE = "chase-jpmorganreserve"
    PNC_BIZ_TRAVELREWARDSVISABUSINESS = "pnc-biz-travelrewardsvisabusiness"
    PNC_SECUREDVISA = "pnc-securedvisa"
    BOA_CUSTOMIZEDCASHREWARDSSECURED = "boa-customizedcashrewardssecured"
    WELLSFARGO_CARRIER = "wellsfargo-carrier"
    CHASE_AMAZON = "chase-amazon"
    BOA_CUSTOMIZEDCASHREWARDSSTUDENTS = "boa-customizedcashrewardsstudents"
    PNC_POINTSVISA = "pnc-pointsvisa"
    AMEX_BIZ_CORPORATEGREEN = "amex-biz-corporategreen"
    WELLSFARGO_HOTELSCOM = "wellsfargo-hotelscom"
    CITI_CASHRETURNS = "citi-cashreturns"
    AMEX_MORGANSTANLEYBLUECASHPREFERRED = "amex-morganstanleybluecashpreferred"
    BOA_UNLIMITEDCASHREWARDSSECURED = "boa-unlimitedcashrewardssecured"
    USBANK_SKYBLUESKYPASS = "usbank-skyblueskypass"
    BOA_UNLIMITEDCASHREWARDSSTUDENTS = "boa-unlimitedcashrewardsstudents"
    BOA_AMSACUSTOMIZEDCASH = "boa-amsacustomizedcash"
    BOA_AMERICARDPOWERREWARDS = "boa-americardpowerrewards"
    CHASE_STARBUCKSREWARDSVISA = "chase-starbucksrewardsvisa"
    AMEX_BIZ_CORPORATEGOLD = "amex-biz-corporategold"
    BOA_MERRILLPLUS = "boa-merrillplus"
    CHASE_DISNEYPREMIER = "chase-disneypremier"
    PNC_CASHUNLIMITED = "pnc-cashunlimited"
    USBANK_BIZ_SKYPASSVISA = "usbank-biz-skypassvisa"
    CHASE_BRITISHAIRWAYS = "chase-britishairways"
    WELLSFARGO_VISASIGNATURE = "wellsfargo-visasignature"
    CHASE_DISNEY = "chase-disney"
    USBANK_ALTITUDEGOSECUREDVISA = "usbank-altitudegosecuredvisa"
    USBANK_ALTITUDEGO = "usbank-altitudego"
    BOA_VISAPLATPLUS = "boa-visaplatplus"
    CAPITALONE_WILLIAMSSONOMA = "capitalone-williamssonoma"
    CAPITALONE_KOHLS = "capitalone-kohls"
    USBANK_BIZ_ALTITUDEPOWER = "usbank-biz-altitudepower"
    CHASE_BIZ_IHGPREMIER = "chase-biz-ihgpremier"
    HSBC_CASHREWARDSSTUDENT = "hsbc-cashrewardsstudent"
    USBANK_HARRISTEETER = "usbank-harristeeter"
    BARCLAYS_ARRIVAL = "barclays-arrival"
    BARCLAYS_ARRIVALPREMIER = "barclays-arrivalpremier"
    CITI_COSTCOANYWHEREVISA = "citi-costcoanywherevisa"
    CITI_HDCOMMERCIALREVOLVING = "citi-hdcommercialrevolving"
    BOA_BIZ_CUSTOMIZEDCASHREWARDS = "boa-biz-customizedcashrewards"
    PNC_BIZ_POINTSVISABUSINESS = "pnc-biz-pointsvisabusiness"
    CHASE_IHGPREMIER = "chase-ihgpremier"
    CHASE_SAPPHIRERESERVE = "chase-sapphirereserve"
    WELLSFARGO_CASHBACKCOLLEGE = "wellsfargo-cashbackcollege"
    CHASE_AMAZONREWARDSVISASIGNATURE = "chase-amazonrewardsvisasignature"
    CHASE_BIZ_SOUTHWESTPREMIER = "chase-biz-southwestpremier"
    USBANK_CASHPLUS = "usbank-cashplus"
    CITI_SIMPLICITY = "citi-simplicity"
    CHASE_BIZ_MARRIOTTBONVOYPREMIERPLUS = "chase-biz-marriottbonvoypremierplus"
    CAPITALONE_JOURNEYSTUDENT = "capitalone-journeystudent"
    AMEX_BIZ_HILTON = "amex-biz-hilton"
    WELLSFARGO_PLATINUMVISA = "wellsfargo-platinumvisa"
    USBANK_BIZ_STARTFARMBIZCASHREWARDS = "usbank-biz-startfarmbizcashrewards"
    BOA_TRAVELREWARDSSECURED = "boa-travelrewardssecured"
    BARCLAYS_ARRIVALPLUS = "barclays-arrivalplus"
    CHASE_UNITEDEXPLORER = "chase-unitedexplorer"
    CHASE_SAPPHIREPREFERRED = "chase-sapphirepreferred"
    USBANK_SKYPASSVISA = "usbank-skypassvisa"
    CHASE_AERLINGUS = "chase-aerlingus"
    CAPITALONE_KEYREWARDS = "capitalone-keyrewards"
    BOA_BIZ_UNLIMITEDCASHREWARDSSECURED = "boa-biz-unlimitedcashrewardssecured"
    CHASE_MARRIOTTBOUNTIFUL = "chase-marriottbountiful"
    PNC_CASHBUILDER = "pnc-cashbuilder"
    BARCLAYS_PRICELINEVIP = "barclays-pricelinevip"
    PNC_BIZ_CASHREWARDSVISABUSINESS = "pnc-biz-cashrewardsvisabusiness"
    AMEX_MARRIOTTBONVOYBEVY = "amex-marriottbonvoybevy"