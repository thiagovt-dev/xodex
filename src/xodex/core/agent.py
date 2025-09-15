from typing import Dict, List
from xodex.config import cfg
from xodex.prompts.system import get_system_prompt
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


async def respond(history: List[Message], stream: bool = True, mode: str = "normal"):
    ctx = build_context()

    # Adicionar informação sobre o modo ativo ao prompt do sistema
    mode_info = ""
    if mode == "agent":
        mode_info = "\n\n[MODE: AGENT] - Você está no modo agente. Você pode aplicar alterações diretamente nos arquivos e executar comandos quando apropriado."
    elif mode == "ask":
        mode_info = "\n\n[MODE: ASK] - Você está no modo ask. Responda apenas a pergunta específica sem aplicar alterações ou executar comandos."
    else:
        mode_info = "\n\n[MODE: NORMAL] - Você está no modo normal. Forneça orientações e sugestões, mas não aplique alterações automaticamente. IMPORTANTE: Sempre complete sua resposta com uma resposta final, mesmo que não possa executar comandos. Use seu conhecimento para dar a melhor resposta possível."

    system_prompt = get_system_prompt()
    system = (
        system_prompt + mode_info + (f"\n\n[PROJECT CONTEXT]\n{ctx}" if ctx else "")
    )
    messages: List[Message] = [{"role": "system", "content": system}, *history]
    prov = _provider()
    return await prov.chat(messages, stream=stream)
