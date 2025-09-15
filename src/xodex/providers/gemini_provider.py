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
        # Verificar se a resposta foi bloqueada ou se há conteúdo válido
        if res.candidates and len(res.candidates) > 0:
            candidate = res.candidates[0]
            if candidate.content and candidate.content.parts:
                return candidate.content.parts[0].text
            else:
                # Verificar safety ratings se a resposta foi bloqueada
                if candidate.safety_ratings:
                    blocked_reasons = [
                        rating.category
                        for rating in candidate.safety_ratings
                        if rating.probability.name in ["HIGH", "MEDIUM"]
                    ]
                    if blocked_reasons:
                        return f"[erro] Resposta bloqueada por: {', '.join(blocked_reasons)}"
                return "[erro] Resposta vazia ou inválida"
        else:
            return "[erro] Nenhuma resposta gerada"
