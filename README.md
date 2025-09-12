# Xodex (CLI Python) – OpenAI | Gemini | Grok

Xodex é um agente de programação para terminal, com seleção de provedor e ferramentas básicas (ler/escrever arquivos, executar comandos) e injeção de **contexto de projeto** por glob.

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

## Notas de segurança
- `:tool run` pede confirmação por padrão. Para comandos destrutivos, revise e confirme conscientemente.


---

## Instalação global via `pipx`
```bash
pipx install .
# depois
xodex
```

Para atualizar a partir de um diretório local:
```bash
pipx reinstall xodex-cli --pip-args='-U .'
```

## Uso com Docker
```bash
docker build -t xodex-cli:local .
docker run --rm -it --env-file .env -v "$PWD":/work -w /work xodex-cli:local
```
Dica: monte seu repositório em `/work` para o agente ter acesso ao contexto e às ferramentas (`:tool run`, `:git ...`).
