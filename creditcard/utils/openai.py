from creditcard.enums import PurchaseCategory, RewardUnit, Benefit, Vendors, APRType, CreditCardKeyword
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
    Avoid duplicating the categories or vendors associated with the rewards.

    valid values for the "amount" json field:
    A small positive number that represents the number of points awarded to the transaction. 
    This number should be between 0 and 100. We are ignoring sign-on bonuses 

    Here is the text you should analyze:
    "{card_attributes}"

    """

import json

def reward_category_map_response_format():
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
                                "category": {
                                    "type": "string",
                                    "enum": [purchase_category.value for purchase_category in PurchaseCategory] + [vendor.value for vendor in Vendors],
                                    "description": '''The category or vendor of the credit card reward. 
                                                    If you want to capture default rewards, use the general category.
                                                    For example, a grocery/dining oriented card might have 3 percent cash
                                                    back on dining/grocery purchases, but only 1 percent cash back on all other purchases. 
                                                    '''
                                },
                                "reward_unit": {
                                    "type": "string",
                                    "enum": [reward_unit.value for reward_unit in RewardUnit if reward_unit != RewardUnit.PERCENT_CASHBACK_USD],
                                },
                                "reward_amount": {
                                    "type": "number",
                                    "description": "The amount of the reward unit. Please use general category amount if you want to capture default rewards. This number is almost always less than 10, and usually aroudn 1-3."
                                },
                                "reward_threshold": {
                                    "type": "object",
                                    "properties": {
                                        "on_up_to_purchase_amount_usd": {
                                            "type": "number",
                                            "description": "The maximum amount of the transaction that the reward is valid for per timeframe. Make this number -1 if there is no limit."
                                        },
                                        "per_timeframe_num_months": {
                                            "type": "number",
                                            "description": "The number of months the reward is valid for, until it resets. Typically a single month but can be greater than 1. Make this number -1 if there is no limit."
                                        },
                                        "fallback_reward_amount": {
                                            "type": "number",
                                            "description": "The fallback amount of the reward unit after the on_up_to_purchase_amount_usd is exceeded in the per_timeframe_num_months months timeframe. Typically the same as reward amount in general category.Make this number -1 if there is no limit."
                                        }   
                                    },
                                    "additionalProperties": False,
                                    "required": ["on_up_to_purchase_amount_usd", "per_timeframe_num_months", "fallback_reward_amount"],
                                }
                            },
                            "required": ["category", "reward_unit", "reward_amount", "reward_threshold"],
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
def conditional_sign_on_bonus_prompt(card_attributes):
    return f"""
    Your task is to extract any and all conditional sign-on bonuses described in the following credit card details. Conditional sign-on bonuses are typically bonuses that require certain actions to be completed (e.g., spending a specific amount within a time frame) in order to qualify.
    Timeframe should be a number that represents months 

    Here is the text you need to analyze:
    "{card_attributes}"

    """

def conditional_sign_on_bonus_response_format():
    return {"type": "json_schema",
            "json_schema": {
                "name": "conditional_sign_on_bonus_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "conditional_sign_on_bonus": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "purchase_type": {"type": "string", "enum": [purchase_category.value for purchase_category in PurchaseCategory if purchase_category != PurchaseCategory.UNKNOWN] + [vendor.value for vendor in Vendors if vendor != Vendors.UNKNOWN]},
                                    "condition_amount": {"type": "number"},
                                    "timeframe": {"type": "number"},
                                    "reward_type": {"type": "string", "enum": [reward_unit.value for reward_unit in RewardUnit if reward_unit != RewardUnit.PERCENT_CASHBACK_USD and reward_unit != RewardUnit.UNKNOWN]},
                                    "reward_amount": {"type": "number"}
                                },
                                "required": ["purchase_type", "condition_amount", "timeframe", "reward_type", "reward_amount"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["conditional_sign_on_bonus"],
                    "additionalProperties": False,
                },
                "strict": True
            },
        }

def apr_prompt(card_attributes):
    return f"""
    Your task is to extract any and all APRs described in the following credit card details.
    Output a list of APRs that have type and amount attributes.

    Here is the text you need to analyze:
    "{card_attributes}"

    """

def apr_response_format():
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "apr_response",
            "schema": {
                "type": "object",
                "properties": {
                    "apr_list": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "apr": {
                                    "type": "number",
                                    "description": "APR must be a positive value less than 100"
                                },
                                "apr_type": {
                                    "type": "string",
                                    "enum": [apr_type.value for apr_type in APRType],
                                    "description": "The type of APR"
                                }
                            },
                            "required": ["apr", "apr_type"],
                            "additionalProperties": False,
                        }
                    }
                },
                "required": ["apr_list"],
                "additionalProperties": False,
            },
            "strict": True
        }
    }

def annual_fee_prompt(card_attributes):
    return f"""
    Your task is to identify and extract any mentioned annual fees from the following credit card details, along with information on how long, if at all, the annual fee is waived after sign-up.
    For example if you see "Low $95 annual fee." that means fee_usd should be 95
    If you see no annual fee, then fee_usd should be 0. 

    Here is the text describing the credit card you need to analyze:
    "{card_attributes}"

    """

def annual_fee_response_format():
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "annual_fee_response",
            "schema": {
                "type": "object",
                "properties": {
                    "annual_fee": {
                        "type": "object",
                        "properties": {
                            "fee_usd": {
                                "type": "number",
                                "description": "amount of annual fee in USD"
                            },
                            "waived_for": {
                                "type": "number",
                                "description": "number of years the annual fee is waived for after sign-up, non-negative number typically 0 or 1 but may be greater than 1"
                            }
                        },
                        "required": ["fee_usd", "waived_for"],
                        "additionalProperties": False,
                    }
                },
                "required": ["annual_fee"],
                "additionalProperties": False,
            },
            "strict": True
        }
    }

def card_keywords_prompt(card_attributes):
    return f"""
    Your task is to identify and extract any mentioned keywords from the following credit card details. 
    Output a list of keywords that have been mentioned in the text.

    Here is the text you need to analyze:
    "{card_attributes}"

    """

def card_keywords_response_format():
    return {"type": "json_schema",
            "json_schema": {
                "name": "card_keywords_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "card_keywords": {
                            "type": "array",
                            "items": {
                                    "type": "string",
                                    "enum": [keyword.value for keyword in CreditCardKeyword],
                                    "description": "keywords that have been mentioned or implied in the text about credit cards"
                            }
                        }
                    },
                    "required": ["card_keywords"],
                    "additionalProperties": False,
                },
                "strict": True
            },
        }

def statement_credit_prompt(card_attributes):
    return f"""
    Your task is to extract any and all annual statement credits described in the following credit card details.
    Note that statement credits which are associated with sign-on bonuses are not considered statement credits.
    We have a separate sign on bonus object, and you should ignore sign on bonuses for this object. It is fine if the list is empty. 

    Here is the text describing a credit card that you need to analyze:
    "{card_attributes}"

    """

def periodic_statement_credit_response_format():
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "periodic_statement_credit_response",
            "schema": {
                "type": "object",
                "properties": {
                    "periodic_statement_credit": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "credit_amount": {"type": "number"},
                                "unit": {
                                    "type": "string",
                                    "enum": [
                                        unit.value for unit in RewardUnit if unit != RewardUnit.UNKNOWN and unit != RewardUnit.PERCENT_CASHBACK_USD
                                    ],
                                    "description": "The unit of the statement credit, usually dollars",
                                },
                                "categories": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": [
                                            category.value
                                            for category in PurchaseCategory
                                            if category != PurchaseCategory.UNKNOWN
                                        ],
                                    },
                                    "description": "Purchase Categories that the statement credit can be spent on.",    
                                },
                                "vendors": {
                                    "type": "array",
                                    "items": {
                                        "type": "string",
                                        "enum": [
                                            vendor.value
                                            for vendor in Vendors
                                            if vendor != Vendors.UNKNOWN
                                        ],
                                    },
                                    "description": "Vendors that the statement credit can be spent at.",
                                },
                                "timeframe_months": {"type": "integer", "description": "Number of months the credit is valid for, before it disappears. MUST BE GREATER THAN ZERO."},
                                "max_uses": {"type": "integer", "description": "Number of times the credit can be used"},
                                "description": {"type": "string", "description": "Human readable description of the statement credit (amount, condition, timeframe, etc.)"},
                            },
                            "required": [
                                "credit_amount",
                                "unit",
                                "categories",
                                "vendors",
                                "timeframe_months",
                                "max_uses",
                                "description",
                            ],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": ["periodic_statement_credit"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
