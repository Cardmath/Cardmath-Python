from openai import OpenAI
from pydantic import BaseModel, TypeAdapter
from typing import Union


import os
import traceback

MODEL = "gpt-4o"

def prompt_openai_for_json(prompt, response_format):
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


def structure_with_openai(prompt: str, response_format: str, schema: Union[BaseModel, TypeAdapter]):
    attempt = 0
    while True:
        if attempt >= 2:
            print("OpenAI failed twice. Aborting.")
            return

        attempt += 1
        openai_response = prompt_openai_for_json(prompt=prompt, response_format=response_format)
        validated_schema = None
        try:
            if isinstance(schema, TypeAdapter):
                validated_schema = schema.validate_json(openai_response)
            else :
                validated_schema = schema.model_validate_json(openai_response)

        except Exception as e:
            print(f"OpenAI failed with attempt {attempt}: {e}")
            continue

        return validated_schema