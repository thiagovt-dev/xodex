# CLI Agente de IA (Python) – OpenAI | Gemini | Grok

Agente de programação para terminal, com seleção de provedor e ferramentas básicas (ler/escrever arquivos, executar comandos) e injeção de **contexto de projeto** por glob.

## Requisitos
- Python 3.10+
- Chaves válidas dos provedores que quiser usar

## Instalação
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
python src/main.py
```

## REPL – Comandos
- `:q` — sair
- `:clear` — limpar histórico
- `:help` — ajuda dos comandos
- `:tool read <path>` — ler arquivo
- `:tool write <path>` — escrever arquivo (digite o conteúdo e finalize com uma linha `EOF`)
- `:tool run <cmd>` — executar comando **com confirmação**
- `:git status` — status do repo
- `:git branches` — lista branches
- `:git checkout <branch>` — muda de branch
- `:git new-branch <name>` — cria e muda para nova branch
- `:git commit "mensagem"` — commit com `git add -A`

## Configuração
- Selecione o provedor em `AGENT_PROVIDER` (`openai`, `gemini`, `grok`).
- Ajuste `CONTEXT_GLOBS` e `MAX_CONTEXT_CHARS` para o tamanho do contexto injetado no prompt.


