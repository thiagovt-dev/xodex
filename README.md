<p align="center">
  <img src="assets/logo_wordmark.png" alt="Xodex" width="380" />
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python 3.10+"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT"></a>
</p>
# Xodex – DeepSeek (default) + OpenAI/Gemini/Grok

Xodex é um agente de programação para terminal. **DeepSeek** é o provedor padrão (economy), mas você também pode usar **OpenAI**, **Gemini** ou **Grok**.



## Providers & Perfis
- **DeepSeek (default)** — custo mínimo e excelente para código/raciocínio.
  - Modelos: `deepseek-reasoner` (R1, raciocínio) ou `deepseek-chat` (V3).
- **OpenAI** — compatível via SDK oficial `openai`.
- **Gemini** — `google-generativeai`.
- **Grok (xAI)** — endpoint compatível OpenAI.

> O Xodex mostra o **modelo em uso** diretamente no prompt de resposta do REPL: `assistant [deepseek-reasoner]> ...`

## Requisitos
- Python 3.10+
- Defina as chaves do(s) provedor(es) que deseja usar

## Instalação (local)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edite .env
```

## Execução
```bash
export PYTHONPATH=.
python -m xodex.main
```

No REPL:
- `:q` — sair
- `:clear` — limpar histórico
- `:help` — ajuda
- `:tool read <path>` — ler arquivo
- `:tool write <path>` — escrever arquivo (finalize com linha `EOF`)
- `:tool run <cmd>` — executar comando **com confirmação**
- `:git status` | `:git branches` | `:git checkout <branch>` | `:git new-branch <name>` | `:git commit "mensagem"`

## Configuração de Providers
Edite `.env` (DeepSeek é o padrão):

```dotenv
# Seleção do provedor (deepseek | openai | gemini | grok)
AGENT_PROVIDER=deepseek

# DeepSeek (padrão)
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_MODEL=deepseek-reasoner
DEEPSEEK_BASE_URL=https://api.deepseek.com

# OpenAI (opcional)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4.1-mini
OPENAI_BASE_URL=https://api.openai.com/v1

# Gemini (opcional)
GEMINI_API_KEY=AIza...
GEMINI_MODEL=gemini-1.5-pro

# Grok (opcional)
GROK_API_KEY=xaI-...
GROK_MODEL=grok-2
GROK_BASE_URL=https://api.x.ai/v1

# Contexto do projeto
CONTEXT_GLOBS=src/**/*.py,**/*.md
MAX_CONTEXT_CHARS=20000
```

## Instalação global via `pipx`
```bash
pipx install .
xodex
```

## Docker
```bash
docker build -t xodex-cli:local .
docker run --rm -it --env-file .env -v "$PWD":/work -w /work xodex-cli:local
```
Dica: monte seu repo em `/work` para o Xodex acessar os arquivos e ferramentas.

---

### Créditos
- Tipografia do wordmark gerada programaticamente para este projeto.
- Ícone e badge simples incluídos em `assets/`.