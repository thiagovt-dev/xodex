from __future__ import annotations
from getpass import getpass
from xodex.config_store import (
    load_config,
    save_config,
    set_api_key,
    get_api_key,
    SUPPORTED,
    DEFAULTS,
    recommended_models,
)


def _ask_provider(default: str) -> str:
    print("\nSelecione o provedor:")
    for i, p in enumerate(SUPPORTED, 1):
        mark = " (padrão)" if p == default else ""
        print(f"  {i}) {p}{mark}")
    while True:
        sel = input("> ").strip() or str(SUPPORTED.index(default) + 1)
        try:
            idx = int(sel) - 1
            if 0 <= idx < len(SUPPORTED):
                return SUPPORTED[idx]
        except ValueError:
            pass
        print("Opção inválida. Tente novamente.")


def _ask_model(provider: str, current: str) -> str:
    opts = recommended_models(provider)
    print(f"\nModelos recomendados para {provider}:")
    for i, m in enumerate(opts, 1):
        star = " *" if m["id"] == DEFAULTS[provider]["model"] else ""
        print(f"  {i}) {m['id']} — {m['label']}{star}")
    print("  c) custom (digitar o ID do modelo)")
    default_ix = 1 + next(
        (
            i
            for i, m in enumerate(opts)
            if m["id"] == (current or DEFAULTS[provider]["model"])
        ),
        0,
    )

    while True:
        sel = input(f"Selecione o modelo [default {default_ix}]: ").strip() or str(
            default_ix
        )
        if sel.lower() == "c":
            val = input("Digite o ID do modelo (ex.: gpt-5): ").strip()
            if val:
                return val
        else:
            try:
                ix = int(sel) - 1
                if 0 <= ix < len(opts):
                    return opts[ix]["id"]
            except ValueError:
                pass
        print("Opção inválida. Tente novamente.")


def _ask_api_key(provider: str) -> str:
    while True:
        key = getpass(f"API key para {provider} (entrada oculta): ").strip()
        if key:
            return key
        print("A chave não pode ser vazia.")


def run_first_time_setup() -> None:
    print("\n🚀 Xodex – configuração inicial")
    cfg = load_config()

    # 1) provider
    prov = _ask_provider(default=cfg.provider or "deepseek")

    # 2) model
    current_model = cfg.providers[prov].model
    model = _ask_model(prov, current_model)

    # 3) salvar config
    cfg.provider = prov
    cfg.providers[prov].model = model
    save_config(cfg)

    # 4) API key
    if not get_api_key(prov):
        key = _ask_api_key(prov)
        backend = set_api_key(prov, key)
        if backend == "file":
            print(
                "! Aviso: keyring indisponível — key salva no config.json (menos seguro)."
            )
        else:
            print("✓ API key salva de forma segura (Keychain do sistema).")

    print(f"✓ Provider padrão: {prov} | modelo: {model}")
    print("Pronto! Você pode reconfigurar a qualquer momento: `xodex setup`.")


def ensure_config_ready() -> None:
    from xodex.config_store import get_api_key
    from xodex.config import (
        cfg as runtime_cfg,
    )

    prov = runtime_cfg["provider"] or "deepseek"
    if not get_api_key(prov) and not runtime_cfg[prov]["api_key"]:
        run_first_time_setup()
