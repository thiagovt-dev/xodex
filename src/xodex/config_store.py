from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional, Dict, List
import json
from platformdirs import user_config_dir
import keyring

APP_NAME = "xodex"
SERVICE_NAME = "xodex"

CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_NAME))
CONFIG_FILE = CONFIG_DIR / "config.json"

SUPPORTED = ("deepseek", "openai", "gemini", "grok")

DEFAULTS = {
    "deepseek": {"model": "deepseek-reasoner"},
    "openai": {"model": "gpt-5"},
    "gemini": {"model": "gemini-2.5-flash"},
    "grok": {"model": "grok-4-0709"},
}

RECOMMENDED = {
    "deepseek": [
        {"id": "deepseek-reasoner", "label": "DeepSeek-V3.1 (Thinking Mode)"},
        {"id": "deepseek-chat", "label": "DeepSeek-V3.1 (Non-thinking)"},
    ],
    "openai": [
        {"id": "gpt-5", "label": "GPT-5 (recente)"},
        {"id": "gpt-4.1", "label": "GPT-4.1"},
        {"id": "gpt-4o", "label": "GPT-4o (multimodal)"},
    ],
    "gemini": [
        {"id": "gemini-2.5-flash", "label": "Gemini 2.5 Flash (rápido)"},
        {"id": "gemini-2.0-pro", "label": "Gemini 2.0 Pro"},
        {"id": "gemini-1.5-pro", "label": "Gemini 1.5 Pro"},
    ],
    "grok": [
        {"id": "grok-4-0709", "label": "Grok-4 (0709)"},
        {"id": "grok-code-fast-1", "label": "Grok Code Fast 1"},
        {"id": "grok-3", "label": "Grok-3"},
        {"id": "grok-3-mini", "label": "Grok-3 mini"},
    ],
}


@dataclass
class ProviderCfg:
    model: str


@dataclass
class AppCfg:
    provider: str
    providers: Dict[str, ProviderCfg]
    keys: Dict[str, str]  # fallback se keyring indisponível

    @staticmethod
    def default() -> "AppCfg":
        return AppCfg(
            provider="deepseek",
            providers={p: ProviderCfg(**DEFAULTS[p]) for p in SUPPORTED},
            keys={},
        )


def _read_json() -> dict:
    if not CONFIG_FILE.exists():
        return {}
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_json(data: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_config() -> AppCfg:
    data = _read_json()
    providers: Dict[str, ProviderCfg] = {}
    for p in SUPPORTED:
        model = data.get("providers", {}).get(p, {}).get("model", DEFAULTS[p]["model"])
        providers[p] = ProviderCfg(model=model)
    provider = data.get("provider", "deepseek")
    keys = data.get("keys", {})
    return AppCfg(provider=provider, providers=providers, keys=keys)


def save_config(cfg: AppCfg) -> None:
    payload = {
        "provider": cfg.provider,
        "providers": {k: asdict(v) for k, v in cfg.providers.items()},
        "keys": cfg.keys,
    }
    _write_json(payload)


def set_api_key(provider: str, key: str) -> str:
    """Salva a key no keyring; se falhar, salva em config.json (fallback). Retorna 'keyring' ou 'file'."""
    try:
        keyring.set_password(SERVICE_NAME, provider, key)
        return "keyring"
    except Exception:
        data = _read_json()
        data.setdefault("keys", {})[provider] = key
        _write_json(data)
        return "file"


def get_api_key(provider: str) -> Optional[str]:
    try:
        val = keyring.get_password(SERVICE_NAME, provider)
        if val:
            return val
    except Exception:
        pass
    data = _read_json()
    return data.get("keys", {}).get(provider)


def recommended_models(provider: str) -> List[dict]:
    return RECOMMENDED.get(provider, [])
