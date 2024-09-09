# Run this way

Install Postman with

On Mac:

```
curl -o- "https://dl-cli.pstmn.io/install/osx_arm64.sh" | sh
```

On Linux
```
curl -o- "https://dl-cli.pstmn.io/install/linux64.sh" | sh
```

Send JSON requests with the form as given by the ExampleRequest classes that inherit pydantic BaseModel

export PYTHONPATH=$(pwd)
fastapi dev app.py

# Sample Output

```
Found 80 cards.
Long description used: 31
Mid description used: 49
 --- 1 ---
 --- 2 ---
CreditCard(name=Bank of America Premium Rewards credit card, issuer=Bank of America, rewards=[(<PurchaseCategory.TRAVEL: 'Travel'>, (<RewardUnit.BANK_OF_AMERICA_PREFERRED_REWARDS: 'Bank of America Preferred Rewards'>, 2.0)), (<PurchaseCategory.DINING: 'Dining'>, (<RewardUnit.BANK_OF_AMERICA_PREFERRED_REWARDS: 'Bank of America Preferred Rewards'>, 2.0)), (None, (<RewardUnit.BANK_OF_AMERICA_PREFERRED_REWARDS: 'Bank of America Preferred Rewards'>, 1.5))], benefits=['global entry/tsa precheck credit', 'no foreign transaction fees', 'travel insurance'], credit_needed=[<CreditNeeded.EXCELLENT: 'Excellent'>, <CreditNeeded.GOOD: 'Good'>])
------------------------------
CreditCard(name=Citi/ AAdvantage Business™World Elite Mastercard, issuer=Citi, rewards=[(<PurchaseCategory.TRAVEL: 'Travel'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 2.0)), (<PurchaseCategory.GAS_AND_TRANSPORTATION: 'Gas and Transportation'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 2.0)), (<PurchaseCategory.UTILITIES_AND_SERVICES: 'Utilities and Services'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 2.0)), (<PurchaseCategory.ELECTRONICS_AND_TECHNOLOGY: 'Electronics and Technology'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 2.0)), (<PurchaseCategory.RETAIL_SHOPPING: 'Retail Shopping'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 1.0)), (<PurchaseCategory.DINING: 'Dining'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 1.0)), (<PurchaseCategory.GROCERIES: 'Groceries'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 1.0)), (<PurchaseCategory.ENTERTAINMENT: 'Entertainment'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 1.0)), (<PurchaseCategory.HEALTH_AND_WELLNESS: 'Health and Wellness'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 1.0)), (<PurchaseCategory.ONLINE_SHOPPING: 'Online Shopping'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 1.0)), (<PurchaseCategory.CHARITABLE_DONATIONS: 'Charitable Donations'>, (<RewardUnit.AA_ADVANTAGE_MILES: 'American Airlines AAdvantage Miles'>, 1.0))], benefits=['free checked bags', 'no foreign transaction fees', 'priority boarding'], credit_needed=[<CreditNeeded.EXCELLENT: 'Excellent'>])
```