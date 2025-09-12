from typing import Dict
from openai import OpenAI
from xodex.config import cfg

Message = Dict[str, str]

client = OpenAI(
    api_key=cfg["deepseek"]["api_key"],
    base_url=cfg["deepseek"]["base_url"],
)  # type: ignore


async def chat(messages: list[Message], stream: bool = True):
    model = cfg["deepseek"]["model"] or "deepseek-reasoner"
    if stream:
        return client.chat.completions.create(
            model=model, messages=messages, stream=True
        )
    else:
        comp = client.chat.completions.create(model=model, messages=messages)
        return comp.choices[0].message.content or ""
