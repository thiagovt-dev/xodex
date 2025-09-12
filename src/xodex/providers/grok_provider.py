from typing import Dict
import requests
from xodex.config import cfg

Message = Dict[str, str]


async def chat(messages: list[Message], stream: bool = True):
    url = f"{cfg['grok']['base_url'].rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {cfg['grok']['api_key']}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": cfg["grok"]["model"],
        "messages": messages,
        "stream": stream,
    }
    resp = requests.post(url, headers=headers, json=payload, stream=stream, timeout=600)
    resp.raise_for_status()
    if stream:
        return resp.iter_lines()
    else:
        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
