
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
Na primeira execução, caso o core Python ainda não esteja instalado, o wrapper tentará instalá-lo automaticamente usando `pipx` ou `pip`.

Requisitos:
- **Node.js >= 18**
- **Python 3.8+** disponível no sistema

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

## 📚 Links úteis
- Core Python (repositório principal): [github.com/thiagovt-dev/xodex](https://github.com/thiagovt-dev/xodex)
- Reportar problemas: [Issues](https://github.com/thiagovt-dev/xodex/issues)

---

## 📄 Licença
[MIT](./LICENSE) © Thiago Vasconcelos Teixeira
