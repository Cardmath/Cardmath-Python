from creditcard.enums import PurchaseCategory, RewardUnit, Benefit, Vendors, APRType, CreditCardKeyword, Issuer, Network, CardKey, CreditNeeded
from creditcard.schemas import ConditionalSignOnBonus, APR, PeriodicStatementCredit, RewardCategoryRelation, RewardCategoryMap, AnnualFee
from database.creditcard.creditcard import CreditCard
from pydantic import BaseModel
from typing import List

import json

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import List, TypeVar, Generic

T = TypeVar('T')

class BaseResponse(BaseModel, ABC, Generic[T]):
    @abstractmethod
    def handle_update(self, target: CreditCard) -> None:
        pass

class RewardCategoryMapResponse(BaseResponse[RewardCategoryRelation]):
    reward_category_map: List[RewardCategoryRelation]

    def handle_update(self, target: CreditCard) -> None:
        target.reward_category_map = [r.model_dump() for r in self.reward_category_map]
        # Also update the primary reward unit
        reward_map = RewardCategoryMap(reward_category_map=self.reward_category_map)
        target.primary_reward_unit = reward_map.get_primary_reward_unit()

class ConditionalSignOnBonusResponse(BaseResponse[ConditionalSignOnBonus]):
    conditional_sign_on_bonus: List[ConditionalSignOnBonus]

    def handle_update(self, target: CreditCard) -> None:
        target.sign_on_bonus = [bonus.model_dump() for bonus in self.conditional_sign_on_bonus]

class APRResponse(BaseResponse[APR]):
    apr_list: List[APR]

    def handle_update(self, target: CreditCard) -> None:
        target.apr = [apr.model_dump() for apr in self.apr_list]

class CreditNeededResponse(BaseResponse[CreditNeeded]):
    credit_needed_list: List[CreditNeeded]

    def handle_update(self, target: CreditCard) -> None:
        target.credit_needed = self.credit_needed_list


class BenefitResponse(BaseResponse[Benefit]):
    benefits_list: List[Benefit]

    def handle_update(self, target: CreditCard) -> None:
        target.benefits = [benefit.value for benefit in self.benefits_list]

class PeriodicStatementCreditResponse(BaseResponse[PeriodicStatementCredit]):
    periodic_statement_credit: List[PeriodicStatementCredit]

    def handle_update(self, target: CreditCard) -> None:
        target.statement_credit = [
            credit.model_dump() for credit in self.periodic_statement_credit
        ]

class CreditCardKeywordResponse(BaseResponse[CreditCardKeyword]):
    card_keywords: List[CreditCardKeyword]

    def handle_update(self, target: CreditCard) -> None:
        target.keywords = [keyword.value for keyword in self.card_keywords]

class AnnualFeeResponse(BaseResponse[AnnualFee]):
    fee_usd: float
    waived_for: int

    def handle_update(self, target: CreditCard) -> None:
        target.annual_fee = AnnualFee(
            fee_usd=self.fee_usd,
            waived_for=self.waived_for
        ).model_dump()

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
                                    "enum": [reward_unit.value for reward_unit in RewardUnit if reward_unit != RewardUnit.UNKNOWN and reward_unit != RewardUnit.STATEMENT_CREDIT_USD],
                                },
                                "reward_amount": {
                                    "type": "number",
                                    "description": "The amount of the reward unit. Please use general category amount if you want to capture default rewards. This number is almost always less than 10, and usually aroudn 1-3."
                                },
                                "reward_threshold": {
                                    "type": ["object", "null"],
                                    "properties": {
                                        "on_up_to_purchase_amount_usd": {
                                            "type": "number",
                                            "description": "The maximum amount of the transaction that the reward is valid for per timeframe."
                                        },
                                        "per_timeframe_num_months": {
                                            "type": "number",
                                            "description": "The number of months the reward is valid for, until it resets. Typically a single month (1) but can be greater than 1."
                                        },
                                        "fallback_reward_amount": {
                                            "type": "number",
                                            "description": "The fallback amount of the reward unit after the on_up_to_purchase_amount_usd is exceeded in the per_timeframe_num_months months timeframe. Typically the same as reward amount in general category"
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

def benefits_response_format():
    enum_benefits = json.dumps([benefit.value for benefit in Benefit], ensure_ascii=False)
    return { "type": "json_schema",
            "json_schema": {
                "name": "benefits_list",
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

def annual_fee_response_format():
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "annual_fee",
            "schema": {
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
                },
            "strict": True
        },
    }

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

def credit_needed_response_format():
    return {"type": "json_schema",
            "json_schema": {
                "name": "credit_needed_response",
                "schema": {
                    "type": "object",
                    "properties": {
                        "credit_needed_list": {
                            "type":"array",
                            "description" : "One or two credit needed enum values.",
                            "items": {
                                    "type": "string",
                                    "enum": [credit_needed.value for credit_needed in CreditNeeded],
                                    "description": "Fico score equivalents: CreditNeeded.EXCELLENT: 850, CreditNeeded.GOOD: 719, CreditNeeded.FAIR: 689, CreditNeeded.POOR: 629"
                            }
                        }
                    },
                    "required": ["credit_needed_list"],
                    "additionalProperties": False,
                },
                "strict": True
            },
        }

def statement_credit_response_format():
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

def credit_card_metadata_response_format():
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "CreditCardMetadata",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the supplied credit card. This name should not include the Issuer or Network."
                    },
                    "issuer": {
                        "type": "string",
                        "description": "Issuer of the described credit card.",
                        "enum": [
                            issuer.value
                            for issuer in Issuer
                        ]
                    },
                    "network": {
                        "type": "string",
                        "description": "Network of the described credit card.",
                        "enum": [
                            network.value
                            for network in Network
                        ]
                    },
                    "key": {
                        "type": ["string"],
                        "description": "Optional lowercase identifier: issuer-name. Can also be NOT FOUND.",
                        "enum": [
                            key.value
                            for key in CardKey
                        ]
                    }
                },
                "required": ["name", "issuer", "key", "network"],
                "additionalProperties": False
            },
            "strict": True
        }
    }