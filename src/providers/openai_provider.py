from typing import Dict
from openai import OpenAI
from src.config import cfg

# Initialize OpenAI client - delay initialization to avoid import-time errors
client = None

def get_client():
    global client
    if client is None:
        try:
            client = OpenAI(
                api_key=cfg["openai"]["api_key"],
                base_url=cfg["openai"]["base_url"]
            )
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            # Try with minimal parameters
            client = OpenAI(api_key=cfg["openai"]["api_key"])
    return client

Message = Dict[str, str]

async def chat(messages: list[Message], stream: bool = True):
    client_instance = get_client()
    if stream:
        return client_instance.chat.completions.create(model=cfg["openai"]["model"], messages=messages, stream=True)
    else:
        comp = client_instance.chat.completions.create(model=cfg["openai"]["model"], messages=messages)
        return comp.choices[0].message.content or ""
