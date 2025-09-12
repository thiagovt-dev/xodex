import os
from dotenv import load_dotenv
from xodex.config_store import load_config, get_api_key

load_dotenv()

_appcfg = load_config()
_provider = os.getenv("AGENT_PROVIDER", _appcfg.provider or "deepseek")


def _val(env_name: str, default: str) -> str:
    v = os.getenv(env_name)
    return v if v is not None and v != "" else default


def _key(env_name: str, provider: str) -> str:
    v = os.getenv(env_name)
    if v:
        return v
    k = get_api_key(provider)
    return k or ""


cfg = {
    "provider": _provider,
    "openai": {
        "api_key": _key("OPENAI_API_KEY", "openai"),
        "model": _val("OPENAI_MODEL", _appcfg.providers["openai"].model),
        "base_url": _val("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    },
    "gemini": {
        "api_key": _key("GEMINI_API_KEY", "gemini"),
        "model": _val("GEMINI_MODEL", _appcfg.providers["gemini"].model),
    },
    "grok": {
        "api_key": _key("GROK_API_KEY", "grok"),
        "model": _val("GROK_MODEL", _appcfg.providers["grok"].model),
        "base_url": _val("GROK_BASE_URL", "https://api.x.ai/v1"),
    },
    "deepseek": {
        "api_key": _key("DEEPSEEK_API_KEY", "deepseek"),
        "model": _val("DEEPSEEK_MODEL", _appcfg.providers["deepseek"].model),
        "base_url": _val("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    },
    "context": {
        "globs": [
            s.strip() for s in os.getenv("CONTEXT_GLOBS", "").split(",") if s.strip()
        ],
        "max_chars": int(os.getenv("MAX_CONTEXT_CHARS", "20000")),
    },
}
