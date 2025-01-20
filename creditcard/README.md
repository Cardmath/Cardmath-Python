# Credit Card Database Pipeline

The RewardsCC API has rich information for over 3000 credit cards. However, in order to cache or store the API responses, we'd need to pay $200 a month. Their database is incomplete, missing key cards such as BiltRewards, and is mostly comprised of cards offered by credit unions that we unfortunately can't support in the early stages of our startup. Furthermore, OpenAI's structured outputs API is extremely powerful, enabling us to turn unstructured text into JSON format by giving the API detailed human instructions. However, at the same time we don't want to overrely on this external API or the scraped web content, so we need an easy way to "annotate" our data.

This architecture enables simplified human annotation.

Priority list for inclusion in Openai prompt:
1. Attribute-Specific Data
    - Fallback on Text Dump
2. RewardsCC Enrichment (if useAPI)

# Inserting a new Card
### Create Metadata with OpenAI
- name *str* (PRIMARY-KEY)
- issuer *str*
- network [Mastercard, Visa, American Express, Discover]
- rewardscc_key *Optional[keyEnum]* (UNIQUE)

Check if name or rewardscc_key exists in DB - if it does, store a detailed logging message and continue.

### 2. Enrich
Pre-populate with the following if isActive == 1: 

- CreditNeeded:
    - c.creditRange
- Annual Fee: 
    - c.isSignupAnnualFeeWaived
    - c.annualFee
    - c.signUpAnnualFee
- Benefits:
    - c.benefit
    - c.loungeAccess
    - c.isLoungeAccess
    - c.freeHotelNight
    - c.freeCheckedBag
    - c.isFreeCheckedBag
- StatementCredit
    - c.benefit
    - c.signUpStatementCredit
- SignOnBonus
    - c.isSignupBonus
    - c.signupBonusAmount
    - c.signupBonusType
    - c.signupBonusCategory
    - c.signupBonusItem 
    - c.signupBonusSpend
    - c.signupBonusLength
    - c.signupBonusLengthPeriod
- RewardCategoryMap
    - c.spendBonusCategory
    - c.baseSpendAmount
    - c.baseSpendEarnType

### *Appendix*
keyEnum:
```
usbank-latamsecured
usbank-latamvisa
chase-marriottbold
chase-amazonprime
citi-premierpassexpedia
usbank-radissonpremier
citi-simplicitycash
usbank-polaris
pnc-biz-visabusiness
barclays-mastercardblack
capitalone-biz-sparkclassic
pnc-premiertravelervisa
citi-rewardsplusstudent
boa-susankomen
discover-studentchrome
citi-premierpassexpediaelite
discover-cashback
boa-travelrewardsstudents
barclays-breeze
boa-allegiant
boa-celecritycruises
chase-inkpremier
capitalone-quicksilverstudents
amex-morganstanleyplatinum
usbank-cashrewardsvisa
chase-marriottbonvoypremier
usbank-biz-altitudeconnect
citi-biz-costcoanywherevisa
chase-iberia
capitalone-quicksilversecured
citi-radioshack
barclays-ubervisa
usbank-startfarmpremier
usbank-biz-radisson
usbank-latamvisasignature
boa-aaavisasignature
boa-elitevisa
wellsfargo-advisors
chase-marriottbonvoyvisasignature
citi-tsc
usbank-infinite
pnc-biz-businessoptionsvisa
barclays-princesscruises
usbank-biz-leverage
chase-marriottboundless
citi-securedmastercard
capitalone-platinumsecured
tdbank-cashsecured
usbank-smartly
barclays-frontier
capitalone-westelm
discover-studentcashback
amex-marriotbonvoyamex
boa-americardstudent
amex-hiltonsurpass
boa-customizedcashrewards
boa-nyuaacustomizedcash
amex-biz-corporateplatinum
pnc-corevisa
capitalone-savoronestudents
barclays-emiratesskywardspremium
usbank-shoppercashrewards
usbank-securedvisa
usbank-altitudeconnect
barclays-hollandamerica
amex-hilton
amex-hiltonaspire
usbank-cashplussecuredvisa
discover-secured
hsbc-premier
amex-biz-marriottbonvoy
pnc-cashrewardsvisa
boa-alaska
usbank-statefarmgoodneighbor
capitalone-potterybarn
amex-marriottbonvoybrilliant
usbank-biz-triplecash
chase-ihgrewardsclassic
boa-americardsecured
usbank-platinum
boa-uspridecustomized
boa-abavisa
wellsfargo-microcenter
wellsfargo-cashwise
chase-southwestpremier
citi-premier
boa-royalcarribean
usbank-radissonvisa
boa-asiana
chase-sapphire
barclays-emiratesskywards
chase-freedomstudent
wellsfargo-biz-secured
usbank-skypassselect
usbank-collegevisa
citi-bestbuy
usbank-perksplusvisa
tdbank-firstclass
barclays-visaapplerewards
wellsfargo-secured
chase-unitedmileageplusvisa
chase-jpmorganreserve
pnc-biz-travelrewardsvisabusiness
pnc-securedvisa
boa-customizedcashrewardssecured
wellsfargo-carrier
chase-amazon
boa-customizedcashrewardsstudents
pnc-pointsvisa
amex-biz-corporategreen
wellsfargo-hotelscom
citi-cashreturns
amex-morganstanleybluecashpreferred
boa-unlimitedcashrewardssecured
usbank-skyblueskypass
boa-unlimitedcashrewardsstudents
boa-amsacustomizedcash
boa-americardpowerrewards
chase-starbucksrewardsvisa
amex-biz-corporategold
boa-merrillplus
chase-disneypremier
pnc-cashunlimited
usbank-biz-skypassvisa
chase-britishairways
wellsfargo-visasignature
chase-disney
usbank-altitudegosecuredvisa
usbank-altitudego
boa-visaplatplus
capitalone-williamssonoma
capitalone-kohls
usbank-biz-altitudepower
chase-biz-ihgpremier
hsbc-cashrewardsstudent
usbank-harristeeter
barclays-arrival
barclays-arrivalpremier
citi-costcoanywherevisa
citi-hdcommercialrevolving
boa-biz-customizedcashrewards
pnc-biz-pointsvisabusiness
chase-ihgpremier
chase-sapphirereserve
wellsfargo-cashbackcollege
chase-amazonrewardsvisasignature
chase-biz-southwestpremier
usbank-cashplus
citi-simplicity
chase-biz-marriottbonvoypremierplus
capitalone-journeystudent
amex-biz-hilton
wellsfargo-platinumvisa
usbank-biz-startfarmbizcashrewards
boa-travelrewardssecured
barclays-arrivalplus
chase-unitedexplorer
chase-sapphirepreferred
usbank-skypassvisa
chase-aerlingus
capitalone-keyrewards
boa-biz-unlimitedcashrewardssecured
chase-marriottbountiful
pnc-cashbuilder
barclays-pricelinevip
pnc-biz-cashrewardsvisabusiness
amex-marriottbonvoybevy
```