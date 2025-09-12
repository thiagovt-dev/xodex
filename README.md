<p align="center">
  <img src="assets/logo_wordmark.png" alt="Xodex" width="380" />
</p>

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python 3.10+"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT"></a>
</p>

# Xodex – DeepSeek (default) + OpenAI/Gemini/Grok

Xodex é um agente de programação para terminal. **DeepSeek** é o provedor padrão (economy), mas você também pode usar **OpenAI**, **Gemini** ou **Grok**.

> 🔐 **Primeira execução**: o Xodex abre um **wizard interativo** para escolher provedor, modelo e salvar sua **API key** com segurança (Keychain/Keyring).  
> Reabra quando quiser com: `xodex setup`.

---

<details>
<summary><strong>🚀 Instalação sem Python (binários)</strong></summary>

Baixe o binário na <a href="https://github.com/thiagovt-dev/xodex/releases">página de Releases</a> (ou use <code>latest</code>):

**Linux (x86_64)**
```bash
curl -L -o xodex https://github.com/thiagovt-dev/xodex/releases/latest/download/xodex-linux-amd64
chmod +x xodex
./xodex
```

**macOS**
```bash
# Intel
curl -L -o xodex https://github.com/thiagovt-dev/xodex/releases/latest/download/xodex-macos-x64
# Apple Silicon
# curl -L -o xodex https://github.com/thiagovt-dev/xodex/releases/latest/download/xodex-macos-arm64

chmod +x xodex
# Se o Gatekeeper bloquear:
# xattr -d com.apple.quarantine xodex
./xodex
```

**Windows**
1. Baixe `xodex-windows-x64.exe` em Releases (versão **latest**).  
2. Execute: `xodex-windows-x64.exe`

</details>

---

<details>
<summary><strong>🍺 Homebrew (em breve)</strong></summary>

Quando o tap estiver publicado:

```bash
brew tap thiagovt-dev/xodex
brew install xodex
xodex
```
</details>

---

<details>
<summary><strong>📦 NPM (em breve)</strong></summary>

Quando o wrapper estiver publicado:

```bash
npm i -g xodex-cli
xodex
```
</details>

---

<details>
<summary><strong>💻 Instalação para dev (Python)</strong></summary>

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
xodex
```

> Dica: se usar `.env` em dev, o wizard não aparece quando as variáveis já estão no ambiente.
</details>

---

<details>
<summary><strong>🧠 Providers & modelos (defaults)</strong></summary>

- **DeepSeek (default)** → `deepseek-reasoner` (V3.1 Thinking Mode)  
  Alternativa: `deepseek-chat` (V3.1 Non-thinking)
- **OpenAI** → `gpt-5`
- **Gemini** → `gemini-2.5-flash`
- **Grok (xAI)** → `grok-4-0709`

Troque depois com `xodex setup`.

> O Xodex mostra o **modelo ativo** no prompt do REPL:  
> `assistente [deepseek-reasoner]> ...`
</details>

---

<details>
<summary><strong>⌨️ Comandos do REPL</strong></summary>

- `/q` — sair  
- `/clear` — limpar histórico  
- `/help` — ajuda  
- `/read <path>` — ler arquivo  
- `/write <path>` — escrever arquivo (finalize com linha `EOF`)  
- `/run <cmd>` — executar comando **com confirmação**  
- `/agent` — alterna modo agente (ações pedem permissão)  
- `/ask <texto>` — pergunta ao modelo sem usar histórico  
- Git: `/status` | `/branches` | `/checkout <branch>` | `/new-branch <name>` | `/commit "mensagem"`
</details>

---

<details>
<summary><strong>🐳 Docker</strong></summary>

```bash
docker build -t xodex-cli:local .
docker run --rm -it   -v "$PWD":/work -w /work   -v "$HOME/.config/xodex:/root/.config/xodex"   xodex-cli:local
```

- Na primeira execução dentro do container, o wizard roda e persiste em `~/.config/xodex`.
- Monte seu repo em `/work` para o Xodex acessar arquivos e comandos.
</details>

---

<details>
<summary><strong>🤖 CI – Release de binários (GitHub Actions)</strong></summary>

Crie `.github/workflows/release-binaries.yml` para gerar binários em cada tag `v*`:

```yaml
name: Release Binaries
on:
  push:
    tags: ["v*"]

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            py: "3.11"
            target: linux-amd64
            exe: xodex
          - os: macos-13
            py: "3.11"
            target: macos-x64
            exe: xodex
          - os: macos-14
            py: "3.11"
            target: macos-arm64
            exe: xodex
          - os: windows-latest
            py: "3.11"
            target: windows-x64
            exe: xodex.exe

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.py }}
      - run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt pyinstaller
      - name: Build
        shell: bash
        run: |
          ENTRY="src/xodex/__main__.py"
          pyinstaller -F -n xodex "$ENTRY"             --collect-all keyring             --collect-all platformdirs
          mkdir -p upload
          BIN="dist/${{ matrix.exe }}"
          OUT="upload/xodex-${{ matrix.target }}${{ endsWith(matrix.exe, '.exe') and '.exe' or '' }}"
          cp "$BIN" "$OUT"
          chmod +x "$OUT" || true
      - uses: softprops/action-gh-release@v2
        if: startsWith(github.ref, 'refs/tags/')
        with:
          files: upload/*
```
</details>

---

### Créditos
- Tipografia do wordmark gerada programaticamente para este projeto.
- Ícone e badge simples incluídos em `assets/`.
