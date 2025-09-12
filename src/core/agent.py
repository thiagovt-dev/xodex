from typing import Dict, List
from src.config import cfg
from src.prompts.system import SYSTEM_PROMPT
from src.core.context import build_context
from src.providers import openai_provider, gemini_provider, grok_provider

Message = Dict[str, str]

PROV_MAP = {
    "openai": openai_provider,
    "gemini": gemini_provider,
    "grok": grok_provider,
}

def _provider():
    return PROV_MAP.get(cfg["provider"], openai_provider)

async def respond(history: List[Message], stream: bool = True):
    ctx = build_context()
    system = SYSTEM_PROMPT + (f"\n\n[PROJECT CONTEXT]\n{ctx}" if ctx else "")
    messages: List[Message] = [{"role": "system", "content": system}, *history]
    prov = _provider()
    return await prov.chat(messages, stream=stream)
