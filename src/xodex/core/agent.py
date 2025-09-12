from typing import Dict, List
from xodex.config import cfg
from xodex.prompts.system import SYSTEM_PROMPT
from xodex.core.context import build_context
from xodex.providers import openai_provider, gemini_provider, grok_provider
from xodex.providers import deepseek_provider

Message = Dict[str, str]

PROV_MAP = {
    "openai": openai_provider,
    "gemini": gemini_provider,
    "grok": grok_provider,
    "deepseek": deepseek_provider,
}


def _provider():
    return PROV_MAP.get(cfg["provider"], deepseek_provider)


def current_model() -> str:
    """Retorna a string do modelo efetivo com base no provider selecionado."""
    p = cfg["provider"]
    if p == "deepseek":
        return cfg["deepseek"]["model"] or "deepseek-reasoner"
    if p == "openai":
        return cfg["openai"]["model"]
    if p == "gemini":
        return cfg["gemini"]["model"]
    if p == "grok":
        return cfg["grok"]["model"]
    return "unknown-model"


def current_provider() -> str:
    return cfg["provider"]


async def respond(history: List[Message], stream: bool = True):
    ctx = build_context()
    system = SYSTEM_PROMPT + (f"\n\n[PROJECT CONTEXT]\n{ctx}" if ctx else "")
    messages: List[Message] = [{"role": "system", "content": system}, *history]
    prov = _provider()
    return await prov.chat(messages, stream=stream)
