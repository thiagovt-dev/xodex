"""
Testes básicos para o Xodex CLI
"""

import pytest


def test_import_xodex():
    """Testa se o módulo principal pode ser importado"""
    try:
        import xodex

        assert xodex is not None
    except ImportError:
        pytest.fail("Não foi possível importar o módulo xodex")


def test_import_config():
    """Testa se o módulo de configuração pode ser importado"""
    try:
        from xodex import config

        assert config is not None
    except ImportError:
        pytest.fail("Não foi possível importar o módulo config")


def test_import_providers():
    """Testa se os providers podem ser importados"""
    try:
        from xodex.providers import deepseek_provider
        from xodex.providers import openai_provider
        from xodex.providers import gemini_provider
        from xodex.providers import grok_provider

        assert deepseek_provider is not None
        assert openai_provider is not None
        assert gemini_provider is not None
        assert grok_provider is not None
    except ImportError as e:
        pytest.fail(f"Não foi possível importar os providers: {e}")


def test_basic_functionality():
    """Teste básico de funcionalidade"""
    # Teste simples para garantir que o pytest funciona
    assert 1 + 1 == 2
    assert "xodex" in "xodex cli"
    assert len("test") == 4
