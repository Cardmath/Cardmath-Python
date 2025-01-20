def reward_category_map_prompt():
    return f"""
    Your goal is to analyze the provided text that describes credit card benefits and map it to the following transaction types and reward units.
    Avoid duplicating the categories or vendors associated with the rewards.

    valid values for the "amount" json field:
    A small positive number that represents the number of points awarded to the transaction. 
    This number should be between 0 and 100. We are ignoring sign-on bonuses 
    """   


def benefits_prompt():
    return f""" 
    You are operating in a data understanding pipeline. 
    You are being given a string that descrbes a credit card and its benefits in plain english.
    You goal is to output a list of benefits found in the text. 
    You should respond with a list of benefits found in the text.
    This list should consist of benefits from the following list:
    """


def conditional_sign_on_bonus_prompt():
    return f"""
    Your task is to extract any and all conditional sign-on bonuses described in the following credit card details. Conditional sign-on bonuses are typically bonuses that require certain actions to be completed (e.g., spending a specific amount within a time frame) in order to qualify.
    Timeframe should be a number that represents months 
    """


def apr_prompt():
    return f"""
    Your task is to extract any and all APRs described in the following credit card details.
    Output a list of APRs that have type and amount attributes.
    """


def annual_fee_prompt():
    return f"""
    Your task is to identify and extract any mentioned annual fees from the following credit card details, along with information on how long, if at all, the annual fee is waived after sign-up.
    For example if you see "Low $95 annual fee." that means fee_usd should be 95
    If you see no annual fee, then fee_usd should be 0. 
    """


def card_keywords_prompt():
    return f"""
    Your task is to identify and extract any mentioned keywords from the following credit card details. 
    Output a list of keywords that have been mentioned in the text.
    """


def statement_credit_prompt():
    return f"""
    Your task is to extract any and all annual statement credits described in the following credit card details.
    Note that statement credits which are associated with sign-on bonuses are not considered statement credits.
    We have a separate sign on bonus object, and you should ignore sign on bonuses for this object. It is fine if the list is empty. 
    """


def credit_needed_prompt():
    return f"""
    Your task is to extract the recommended credit a customer should have when applying for this card.
    If not information can be found, output null
    """


def credit_card_metadata_prompt(dump):
    return f"""
    Your task is to extract accurate metadata about a credit card based on the provided plain English description. Focus on ensuring all extracted fields are complete, precise, and directly inferred from the input text.

    ### GUIDELINES ###
    1. **Field Descriptions**:
        - `name`: The full official name of the credit card as stated in the description.
        - `issuer`: The financial institution that issues the card (e.g., Chase, Capital One, Amex).
        - `network`: The card's payment network (e.g., Visa, MasterCard, Amex, Discover).
        - `key`: A unique lowercase identifier for the card, formatted as `issuer-name`. Follow these guidelines:
            - Replace spaces with hyphens, remove symbols, and exclude generic terms like "Credit Card" or "Rewards" for standardization.
            - If a key match cannot be confidently determined from the description, always return the placeholder value: `KEY MATCH NOT FOUND`.
            - The `key` must only contain words directly present in the `name`, `issuer`, or `network`. 
            - Do not infer unrelated words (e.g., "student," "marriott") unless explicitly stated in the name or description.
            - If a word like 'flex' is omitted in the key, don't pick it
            - If there is any ambiguity, or if the match seems incorrect, prioritize `KEY MATCH NOT FOUND` over guessing or inferring values.
            - Example: "Gold Card" does not translate to "marriottbonvoy-bevy." Ensure that no unrelated terms are introduced.
            - The goal is accuracy over completion; a missing or ambiguous match should default to `KEY MATCH NOT FOUND`.


    3. **Input Scope**:
        - Analyze the entire description for key phrases that indicate rewards, issuer, network, and card name.

    ### EXAMPLE ###
        ### INPUT ###
        "Chase Sapphire Preferred® Credit Card offers an enticing sign-on bonus of 60,000 points after spending $4,000 on purchases within the first three months of account opening. This card is designed for travelers and dining enthusiasts, featuring 3X points on dining, including eligible delivery services and takeout, and 2X points on other travel purchases. Additionally, cardholders earn 5X points on travel booked through Chase TravelSM, excluding hotels qualifying for the $50 Annual Chase Travel Hotel Credit. With a competitive variable APR range of 20.49% to 27.49% and an annual fee of $95, this card combines premium rewards with valuable perks tailored for frequent travelers and diners."
        
        ### OUTPUT ### 
            name: Chase Sapphire Preferred® Credit Card
            issuer: Chase
            network: Visa
            key: chase-sapphirepreferred
    ### END EXAMPLE ### 

    ### INPUT ###
    {dump}

    ### TASK ###
    Extract and return:
    - `name`
    - `issuer`
    - `network`
    - `key`
    """
