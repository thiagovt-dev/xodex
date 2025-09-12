from typing import Dict
from openai import OpenAI
from xodex.config import cfg

client = OpenAI(api_key=cfg["openai"]["api_key"], base_url=cfg["openai"]["base_url"])  # type: ignore

Message = Dict[str, str]


async def chat(messages: list[Message], stream: bool = True):
    if stream:
        return client.chat.completions.create(
            model=cfg["openai"]["model"], messages=messages, stream=True
        )
    else:
        comp = client.chat.completions.create(
            model=cfg["openai"]["model"], messages=messages
        )
        return comp.choices[0].message.content or ""
