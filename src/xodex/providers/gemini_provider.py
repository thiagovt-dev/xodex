import google.generativeai as genai
from xodex.config import cfg
from typing import Dict

Message = Dict[str, str]

genai.configure(api_key=cfg["gemini"]["api_key"])
model = genai.GenerativeModel(cfg["gemini"]["model"])  # type: ignore


def _map_to_gemini(messages: list[Message]):
    sys = "\n".join([m["content"] for m in messages if m["role"] == "system"]) or ""
    history = [
        {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
        for m in messages
        if m["role"] != "system"
    ]
    return sys, history


async def chat(messages: list[Message], stream: bool = True):
    sys, history = _map_to_gemini(messages)
    chat = model.start_chat(history=history)
    if stream:
        res = chat.send_message(sys, stream=True)
        return res
    else:
        res = chat.send_message(sys)
        return res.text
