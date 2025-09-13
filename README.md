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

<!-- ---

<details>
<summary><strong>🍺 Homebrew (em breve)</strong></summary>

Quando o tap estiver publicado:

```bash
brew tap thiagovt-dev/xodex
brew install xodex
xodex
```
</details> -->

---

<details>
<summary><strong>📦 NPM</strong></summary>

Instale o wrapper globalmente e rode o Xodex:

```bash
npm i -g @thiagovt-dev/xodex-cli
xodex --help
```

✅ Na **primeira execução**, o wrapper prepara automaticamente o core em Python
(preferindo **pipx**; sem necessidade de venv).
Requisitos: **Node >= 18** e **Python >= 3.8** no sistema.

</details>

<details>
<summary><strong>🛠️ Dicas (Linux/PEP 668)</strong></summary>

Se aparecer aviso de "externally-managed environment", instale o <code>pipx</code>:

```bash
sudo apt update && sudo apt install -y pipx
pipx ensurepath
exec $SHELL -l
```

Depois, basta rodar:

```bash
xodex --help
```

</details>

<details>
<summary><strong>⬆️ Atualizar</strong></summary>

```bash
npm i -g @thiagovt-dev/xodex-cli@latest
# (opcional) atualizar o core Python gerenciado pelo pipx
pipx upgrade xodex || pipx install xodex-cli --force
```

</details>

---

<details>
<summary><strong>🐍 PyPI</strong></summary>

Instale diretamente do PyPI:

```bash
pip install xodex-cli
xodex --help
```

**Recomendado:** use `pipx` para evitar conflitos com outros pacotes:

```bash
pipx install xodex-cli
xodex --help
```

> 💡 **Dica:** O `pipx` isola o Xodex em seu próprio ambiente virtual, evitando conflitos de dependências.

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


## 🤝 Contribuindo

Contribuições são muito bem-vindas! Este projeto está aberto para a comunidade e aceita:

- 🐛 **Reportes de bugs**
- ✨ **Sugestões de novas funcionalidades**
- 📝 **Melhorias na documentação**
- 🔧 **Novos providers de IA**
- 🧪 **Testes e melhorias de qualidade**

### Como contribuir:

1. **Fork** o repositório
2. **Clone** seu fork: `git clone https://github.com/SEU_USUARIO/xodex.git`
3. **Crie** uma branch: `git checkout -b feature/nova-funcionalidade`
4. **Faça** suas alterações seguindo o [guia de contribuição](CONTRIBUTING.md)
5. **Teste** suas mudanças: `ruff check . && black --check . && pytest`
6. **Commit** com Conventional Commits: `git commit -m "feat: adiciona novo provider"`
7. **Push** para sua branch: `git push origin feature/nova-funcionalidade`
8. **Abra** um Pull Request

### Padrões de código:
- **Formatação:** Black
- **Lint:** Ruff
- **Testes:** Pytest
- **Commits:** Conventional Commits

📖 **Leia mais:** [CONTRIBUTING.md](CONTRIBUTING.md) | [Código de Conduta](CODE_OF_CONDUCT.md) | [Política de Segurança](SECURITY.md)

---

## ⚠️ Aviso Legal

**Xodex não é afiliado a OpenAI, Google, xAI, DeepSeek ou qualquer outro provedor de IA.** Este é um projeto independente desenvolvido pela comunidade.

---

### Créditos

**Xodex** foi desenvolvido por [Thiago Vasconcelos](https://github.com/thiagovt-dev), um desenvolvedor Full-Stack apaixonado por criar soluções inovadoras.
