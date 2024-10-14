from creditcard.enums import PurchaseCategory, RewardUnit, Benefit
from dotenv import load_dotenv
from openai import OpenAI
import json
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

separator = "\n - "

def prompt_gpt4_for_json(prompt):    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
                "max_tokens" : 2000,
                "temperature" : 0.0
            }
        ],
        model="gpt-4o",
    )
    return chat_completion.choices[0].message.content

def retry_openai_until_json_valid(prompt, card_attr_list_joined):
    attempt = 0
    reward_category_map = {}
    card_attr_list_joined = f"""
    Reward Program Name	Travel	Dining	Groceries	Gas and Transportation	Entertainment	Retail Shopping	Utilities and Services	Health and Wellness	Electronics and Technology	Charitable Donations	Online Shopping
TravelMax Rewards	3	1	2	1	2	2	1	2	1	3	1
DiningDelight Program	2	3	1	1	1	2	2	1	2	1	3
GrocerySaver Points	1	2	3	2	1	1	1	2	3	2	2
FuelSaver Rewards	1	1	2	3	2	1	2	3	1	2	1
EntertainmentElite	2	1	1	2	3	3	1	2	2	1	2
ShopSmart Rewards	1	2	2	1	1	3	3	1	3	2	1
HealthPlus Points	3	1	1	2	1	2	1	3	2	1	2
TechSavvy Rewards	1	2	2	3	1	1	2	1	3	2	3
CharityChamp Program	2	3	1	1	1	1	2	2	1	3	1
OnlineShopping Advantage	1	2	3	2	2	1	1	1	2	2	3"""

    while True:
        attempt += 1
        openai_response = prompt_gpt4_for_json(prompt(card_attr_list_joined))    
        try:
            reward_category_map = json.loads(openai_response)
        except ValueError:
            continue
        break
    
    print(reward_category_map)
    print(f"OpenAI succeeded with attempt {attempt}")    
    return reward_category_map

def purchase_category_map_prompt(card_attributes) : 
    return f"""
    You are operating in a data understanding pipeline. 
    Please analyze the provided text that describes credit card benefits and map it to the following transaction types and reward units.
    Return the mapped transaction types and reward units as JSON objects. 

    TRANSACTION TYPES / PURCHASE CATEGORIES:
    {separator.join([purchase_category.value for purchase_category in PurchaseCategory])}

    REWARD UNITS / POINTS SYSTEMS:
    {separator.join([reward_unit.value for reward_unit in RewardUnit])}

    CREDIT CARD BENEFITS RAW TEXT:
    "{card_attributes}"

    OUTPUT:
    I want you to respond in correct Javascript as if answering an API call. 
    You should not use ```javascript to indicate you are writing javascript. 
    The returned JSON dictionary should represent the amount of 'reward unit' when spending $1 on a purchase belonging to a specific category. 
    It is reasonable to assume that the lowest value is 1 for all reward units.

    EXAMPLE OUTPUT ELEMENT: 
    "Groceries" : ("Hilton Honors Points", 3)
    "Gas" : ("Hilton Honors Points", 1)
    "Gas" : ("Hilton Honors Points", 1)

    EXAMPLE OUTPUT EXPLANATION:
    each dollar spent on food and drink groceries transactions earns you 3 Hilton Honors Points
    """


def benefits_prompt(card_dict_attr_list) : 
    return f""" 
    You are operating in a data understanding pipeline. 
    You are being given a string that descrbes a credit card and its benefits in plain english.
    You goal is to output a list of benefits found in the text. 
    You should respond with a list of benefits found in the text.
    This list should consist of benefits from the following list:
    
    CREDIT CARD BENEFITS ENUM LIST :
    {separator.join([benefit.value for benefit in Benefit])}

    EXAMPLE OUTPUT:
    airport lounge access, cell phone protection, concierge service
    
    
    Now I will start with the text that you should analyze:
    
    "{card_dict_attr_list}"
    
    """  
