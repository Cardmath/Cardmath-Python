from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

def prompt_gpt4_for_json(prompt):    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(chat_completion.choices[0].message.content)
    return chat_completion.choices[0].message.content

benefits_prompt = lambda card_dict_attr_list : f"""
Please extract which of the following credit card benefits are mentioned in the provided text. If a benefit is present, list it in the output.

Credit Card Benefits:
- "airport lounge access"
- "cell phone protection"
- "concierge service"
- "emergency medical insurance"
- "event ticket access"
- "extended return period"
- "extended warranty"
- "free checked bags"
- "global entry/tsa precheck credit"
- "no foreign transaction fees"
- "price protection"
- "priority boarding"
- "purchase protection"
- "rental car insurance"
- "return protection"
- "travel assistance services"
- "travel insurance"

Text: "{card_dict_attr_list}"

The output should be a list of benefits found in the text, in a comma separated list format with just the enum name such as:
airport lounge access, cell phone protection, concierge service etc.
"""
