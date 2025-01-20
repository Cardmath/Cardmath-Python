from creditcard.structure.openai import utils
from database.creditcard.creditcard import CreditCard
from database.creditcard.source import CreditCardSource, UpdateableSourceColumns
from pydantic import BaseModel
from typing import Union
from creditcard.enums import CardKey
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Callable, Type, Optional, Literal

from creditcard.schemas import CreditCardKeyMetadata 
import creditcard.structure.openai.prompts as prompts
import creditcard.structure.openai.schemas as resp_schemas
import creditcard.structure.rewardsccapi as enrich 

import json

DIRECT_PREAMBLE = "All information in the provided text refers to the object you are assigned to parse."
DUMP_PREAMBLE = "This is all information we found about the credit card. Some text might not be necessary to parse the assigned object. \
    Use your best judgement to only extract necessary fields."
ENRICHMENT = "In addition, we have a JSON object with information pertaining to the card that was sourced from a 3rd party API:"

T = TypeVar('T', bound=resp_schemas.BaseResponse)

class BaseTargetUpdate(BaseModel, Generic[T]):
    """
    Base class for all target updates, parameterized by response type T
    Returns a list (often a singleton) of updates to perform based on changes 
    to the source table
    """
    field_name: UpdateableSourceColumns
    field_prompt: str
    response_format: dict
    rewardscc_extract: Callable[[dict], str]
    response_model: Type[T]

class AnnualFeeUpdate(BaseTargetUpdate[resp_schemas.AnnualFeeResponse]):
    field_name: Union[Literal[UpdateableSourceColumns.ANNUAL_FEE], Literal[UpdateableSourceColumns.DUMP]]
    
    @classmethod
    def create(cls, field_name: UpdateableSourceColumns = UpdateableSourceColumns.ANNUAL_FEE) -> 'AnnualFeeUpdate':
        return cls(
            field_name=field_name,
            field_prompt=prompts.annual_fee_prompt(),
            response_format=resp_schemas.annual_fee_response_format(),
            rewardscc_extract=enrich.extract_annual_fee,
            response_model=resp_schemas.AnnualFeeResponse
        )

class RewardCategoryUpdate(BaseTargetUpdate[resp_schemas.RewardCategoryMapResponse]):
    field_name: Union[Literal[UpdateableSourceColumns.REWARD_CATEGORY_MAP], Literal[UpdateableSourceColumns.DUMP]]
    
    @classmethod
    def create(cls, field_name: UpdateableSourceColumns = UpdateableSourceColumns.REWARD_CATEGORY_MAP) -> 'RewardCategoryUpdate':
        return cls(
            field_name=field_name,
            field_prompt=prompts.reward_category_map_prompt(),
            response_format=resp_schemas.reward_category_map_response_format(),
            rewardscc_extract=enrich.extract_reward_category_map,
            response_model=resp_schemas.RewardCategoryMapResponse
        )

class SignOnBonusUpdate(BaseTargetUpdate[resp_schemas.ConditionalSignOnBonusResponse]):
    field_name: Union[Literal[UpdateableSourceColumns.SIGN_ON_BONUS], Literal[UpdateableSourceColumns.DUMP]]
    
    @classmethod
    def create(cls, field_name: UpdateableSourceColumns = UpdateableSourceColumns.SIGN_ON_BONUS) -> 'SignOnBonusUpdate':
        return cls(
            field_name=field_name,
            field_prompt=prompts.conditional_sign_on_bonus_prompt(),
            response_format=resp_schemas.conditional_sign_on_bonus_response_format(),
            rewardscc_extract=enrich.extract_sign_on_bonus,
            response_model=resp_schemas.ConditionalSignOnBonusResponse
        )

class StatementCreditUpdate(BaseTargetUpdate[resp_schemas.PeriodicStatementCreditResponse]):
    field_name: Union[Literal[UpdateableSourceColumns.STATEMENT_CREDIT], Literal[UpdateableSourceColumns.DUMP]]
    
    @classmethod
    def create(cls, field_name: UpdateableSourceColumns = UpdateableSourceColumns.STATEMENT_CREDIT) -> 'StatementCreditUpdate':
        return cls(
            field_name=field_name,
            field_prompt=prompts.statement_credit_prompt(),
            response_format=resp_schemas.statement_credit_response_format(),
            rewardscc_extract=enrich.extract_statement_credit,
            response_model=resp_schemas.PeriodicStatementCreditResponse
        )

class BenefitsUpdate(BaseTargetUpdate[resp_schemas.BenefitResponse]):
    field_name: Union[Literal[UpdateableSourceColumns.BENEFITS], Literal[UpdateableSourceColumns.DUMP]]
    
    @classmethod
    def create(cls, field_name: UpdateableSourceColumns = UpdateableSourceColumns.BENEFITS) -> 'BenefitsUpdate':
        return cls(
            field_name=field_name,
            field_prompt=prompts.benefits_prompt(),
            response_format=resp_schemas.benefits_response_format(),
            rewardscc_extract=enrich.extract_benefits,
            response_model=resp_schemas.BenefitResponse
        )

class APRUpdate(BaseTargetUpdate[resp_schemas.APRResponse]):
    field_name: Union[Literal[UpdateableSourceColumns.APR], Literal[UpdateableSourceColumns.DUMP]]
    
    @classmethod
    def create(cls, field_name: UpdateableSourceColumns = UpdateableSourceColumns.APR) -> 'APRUpdate':
        return cls(
            field_name=field_name,
            field_prompt=prompts.apr_prompt(),
            response_format=resp_schemas.apr_response_format(),
            rewardscc_extract=lambda x: "",
            response_model=resp_schemas.APRResponse
        )
    
class CreditNeededUpdate(BaseTargetUpdate[resp_schemas.CreditNeededResponse]):
    field_name: Union[Literal[UpdateableSourceColumns.APR], Literal[UpdateableSourceColumns.DUMP]]
    
    @classmethod
    def create(cls, field_name: UpdateableSourceColumns = UpdateableSourceColumns.APR) -> 'APRUpdate':
        return cls(
            field_name=field_name,
            field_prompt=prompts.credit_needed_prompt(),
            response_format=resp_schemas.credit_needed_response_format(),
            rewardscc_extract=enrich.extract_credit_needed,
            response_model=resp_schemas.CreditNeededResponse
        )

class KeywordsUpdate(BaseTargetUpdate[resp_schemas.CreditCardKeywordResponse]):
    field_name: Union[Literal[UpdateableSourceColumns.KEYWORDS], Literal[UpdateableSourceColumns.DUMP]]
    
    @classmethod
    def create(cls, field_name: UpdateableSourceColumns = UpdateableSourceColumns.KEYWORDS) -> 'KeywordsUpdate':
        return cls(
            field_name=field_name,
            field_prompt=prompts.card_keywords_prompt(),
            response_format=resp_schemas.card_keywords_response_format(),
            rewardscc_extract=lambda x: "",
            response_model=resp_schemas.CreditCardKeywordResponse
        )
    
class DumpUpdate:

    def create():
        return [update.create(field_name=UpdateableSourceColumns.DUMP.value) for update in 
                [AnnualFeeUpdate,
                 RewardCategoryUpdate,
                 SignOnBonusUpdate,
                 StatementCreditUpdate,
                 BenefitsUpdate,
                 APRUpdate,
                 KeywordsUpdate,
                 CreditNeededUpdate]] 

def get_target_update(field: UpdateableSourceColumns) -> BaseTargetUpdate:
    """
    Returns the appropriate update handler for a given field.
    """
    mapping = {
        UpdateableSourceColumns.ANNUAL_FEE: AnnualFeeUpdate,
        UpdateableSourceColumns.REWARD_CATEGORY_MAP: RewardCategoryUpdate,
        UpdateableSourceColumns.SIGN_ON_BONUS: SignOnBonusUpdate,
        UpdateableSourceColumns.STATEMENT_CREDIT: StatementCreditUpdate,
        UpdateableSourceColumns.BENEFITS: BenefitsUpdate,
        UpdateableSourceColumns.APR: APRUpdate,
        UpdateableSourceColumns.KEYWORDS: KeywordsUpdate,
        UpdateableSourceColumns.CREDIT_NEEDED: CreditNeededUpdate,
        UpdateableSourceColumns.DUMP: DumpUpdate
    }
    
    update_class = mapping.get(field)
    if not update_class:
        raise ValueError(f"No update handler defined for field: {field}")
    
    return update_class.create()

def generate_metadata(dump: str):
    return utils.structure_with_openai(
        prompt=prompts.credit_card_metadata_prompt(dump),
        response_format=resp_schemas.credit_card_metadata_response_format(),
        schema=CreditCardKeyMetadata
    )

class CardKeyResponse(BaseModel):
    key: CardKey

def match_key(metadata: CreditCardKeyMetadata) -> CardKey:
    return utils.structure_with_openai(
        prompt=prompts.credit_card_metadata_prompt(),
        response_format=resp_schemas.credit_card_metadata_response_format(),
        schema=CreditCardKeyMetadata
    )


def update_field(
    update: BaseTargetUpdate[T], 
    source: CreditCardSource, 
    target: CreditCard, 
    rewardscc_dict: Optional[dict], 
) -> None:
    """
    Updates a specific field of a credit card using the provided update handler.
    """
    prompt_list: list[str] = [update.field_prompt]

    preamble=DIRECT_PREAMBLE
    if update.field_name == UpdateableSourceColumns.DUMP.value:
        preamble = DUMP_PREAMBLE

    if getattr(source, update.field_name):
        content = getattr(source, update.field_name)
    else:
        raise Exception(
            f"No source text to parse from. Aborting changes to "
            f"({source.name}, {source.issuer}, {source.network} - {source.key})"
        )
    
    prompt_list.extend([preamble, content])

    # Add enrichment data if available
    if rewardscc_dict:
        enrichment_data = update.rewardscc_extract(rewardscc_dict)
        if enrichment_data:
            prompt_list.extend([ENRICHMENT, json.dumps(enrichment_data)])
    
    # Construct final prompt and get response
    final_prompt = "\n\n".join(prompt_list)
    response = utils.structure_with_openai(
        prompt=final_prompt, 
        response_format=update.response_format, 
        schema=update.response_model
    )
    
    # Use handle_update directly from response
    response.handle_update(target)