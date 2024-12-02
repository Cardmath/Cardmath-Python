from fastapi.responses import StreamingResponse
from chat.schemas import ChatRequest
import openai
import os
from typing import AsyncGenerator

async def generate_stream(message: str) -> AsyncGenerator[bytes, None]:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    MODEL = "gpt-4o-2024-08-06"
    try:
        stream = openai.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": message}],
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"{chunk.choices[0].delta.content}\n\n".encode('utf-8')
        
        yield b"[DONE]\n\n"
        
    except Exception as e:
        print(f"Error in generate_stream: {str(e)}")
        yield f"Error: {str(e)}\n\n".encode('utf-8')

async def chat(request: ChatRequest) -> StreamingResponse:
    return StreamingResponse(
        generate_stream(request.message),
        media_type='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'X-Accel-Buffering': 'no'
        }
    )