from creditcard.enums import PurchaseCategory, RewardUnit, Benefit
from openai import OpenAI
from pydantic import BaseModel, TypeAdapter
from typing import Union
import json
import os
import traceback

separator = "\n - "
MODEL = "gpt-4o-2024-08-06"


async def prompt_openai_for_json(prompt, response_format):    
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY', "your_openai_api_key")
    )
    try:
        chat_completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                    "max_tokens" : 2000,
                    "temperature" : 0.0
                }
            ],
            response_format=response_format
        )
        response= chat_completion.choices[0].message.content
        return response
    
    except Exception as e:
        error_details = traceback.format_exc()
        raise ConnectionError(f"Connection to OpenAI failed: {e}\nDetails: {error_details}")

async def structure_with_openai(prompt: str, response_format: dict, schema: Union[BaseModel, TypeAdapter]):
    attempt = 0
    while True:
        if attempt >= 3:
            print("OpenAI failed 3 times. Aborting.")
            return

        attempt += 1
        openai_response = await prompt_openai_for_json(prompt=prompt, response_format=response_format)  
        validated_schema = None  
        try:
            if isinstance(schema, TypeAdapter):
                validated_schema = schema.validate_json(openai_response)
            else :
                validated_schema = schema.model_validate_json(openai_response)

        except Exception as e:
            print(f"OpenAI failed with attempt {attempt}: {e}")
            continue

        print(f"OpenAI succeeded with attempt {attempt}")
        return validated_schema

def purchase_category_map_prompt(card_attributes) : 
    return f"""
    Your goal is to analyze the provided text that describes credit card benefits and map it to the following transaction types and reward units.

    valid values for the "category" json field:
    {separator.join([purchase_category.value for purchase_category in PurchaseCategory])}

    valid values for the "reward_unit" json field:
    {separator.join([reward_unit.value for reward_unit in RewardUnit])}

    valid values for the "amount" json field:
    A small positive number that represents the number of points awarded to the transaction.

    Here is the text you should analyze:
    "{card_attributes}"

    """

import json

def reward_category_map_response_format():
    enum_category = json.dumps([purhcase_category.value for purhcase_category in PurchaseCategory], ensure_ascii=False)
    enum_reward_unit = json.dumps([reward_unit.value for reward_unit in RewardUnit], ensure_ascii=False)

    return {
        "type": "json_schema",
        "json_schema": {
            "name": "reward_category_map_response",
            "schema": {
                "type": "object",
                "properties": {
                    "reward_category_map": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "category": {"type": "string", "enum": json.loads(enum_category)},
                                "reward_unit": {"type": "string", "enum": json.loads(enum_reward_unit)},
                                "amount": {"type": "number"}
                            },
                            "required": ["category", "reward_unit", "amount"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["reward_category_map"],
                "additionalProperties": False
            },
            "strict": True
        }
    }



def benefits_prompt(card_attributes) : 
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
    
    "{card_attributes}"
    
    """  

def benefits_response_format():
    enum_benefits = json.dumps([benefit.value for benefit in Benefit], ensure_ascii=False)
    return { "type": "json_schema",
            "json_schema": {
                "name": "benefits_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "benefits_list": {"type": "array", "items": {"type": "string", "enum": json.loads(enum_benefits)}},
                    },
                    "required": ["benefits_list"],
                    "additionalProperties": False
                },
                "strict": True
            }
    }