
[![npm version](https://img.shields.io/npm/v/@thiagovt-dev/xodex-cli?color=blue)](https://www.npmjs.com/package/@thiagovt-dev/xodex-cli)
[![downloads](https://img.shields.io/npm/dt/@thiagovt-dev/xodex-cli.svg)](https://www.npmjs.com/package/@thiagovt-dev/xodex-cli)

Wrapper em **Node.js** para o [Xodex](https://github.com/thiagovt-dev/xodex), um utilitário escrito em **Python** que oferece ferramentas de automação, integração com IA e fluxos de desenvolvimento.

Este pacote permite que você instale e execute o **Xodex** diretamente via **npm**, sem precisar lidar manualmente com `pip` ou dependências Python — o wrapper cuida da instalação automática do core quando necessário.

---

## 🚀 Instalação

```bash
npm i -g @thiagovt-dev/xodex-cli
```

O comando `xodex` ficará disponível globalmente.  
Na primeira execução, caso o core Python ainda não esteja instalado, o wrapper tentará instalá-lo automaticamente usando múltiplas estratégias:

1. **pipx** (recomendado para ambientes isolados)
2. **pip com --break-system-packages** (para ambientes externamente gerenciados como Ubuntu/Debian)
3. **pip --user** (instalação tradicional)

Requisitos:
- **Node.js >= 18**
- **Python 3.8+** disponível no sistema
- **pipx** (opcional, mas recomendado para melhor isolamento)

---

## 🛠️ Uso

```bash
xodex --help
```

Exemplos:
```bash
# rodar comando padrão
xodex run

# verificar versão
xodex --version
```

---

## 🔧 Troubleshooting

### Erro "externally-managed-environment"

Se você encontrar o erro `externally-managed-environment` (comum em Ubuntu/Debian), o wrapper tentará automaticamente usar `--break-system-packages`. Se ainda assim falhar, instale manualmente:

```bash
# Opção 1: Usando pipx (recomendado)
pipx install xodex-cli

# Opção 2: Usando pip com --break-system-packages
python3 -m pip install --break-system-packages xodex-cli

# Opção 3: Instalação tradicional
python3 -m pip install --user xodex-cli
```

### Python não encontrado

Se o Python não for encontrado, instale-o:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# macOS (com Homebrew)
brew install python

# Windows
# Baixe do site oficial: https://www.python.org/downloads/
```

### Instalar pipx (recomendado)

```bash
# Ubuntu/Debian
sudo apt install pipx

# macOS
brew install pipx

# Windows
pip install pipx
```

---

## 📚 Links úteis
- Core Python (repositório principal): [github.com/thiagovt-dev/xodex](https://github.com/thiagovt-dev/xodex)
- Reportar problemas: [Issues](https://github.com/thiagovt-dev/xodex/issues)

---

## 📄 Licença
[MIT](./LICENSE) © Thiago Vasconcelos Teixeira
