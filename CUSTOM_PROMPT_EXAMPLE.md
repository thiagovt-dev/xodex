# Como usar o Xodex com Prompt Personalizado

O Xodex usa por padrão o prompt personalizado definido no arquivo `src/xodex/prompts/xodex-cli.txt`. Você também pode sobrescrever esse prompt usando a variável de ambiente `XODEX_SYSTEM_PROMPT`.

## Exemplo de Uso

### 1. Usar o prompt padrão (recomendado)

O Xodex já vem com um prompt personalizado otimizado no arquivo `xodex-cli.txt`. Basta executar:

### 2. Executar o Xodex

```bash
cd /caminho/para/seu/projeto
xodex
```

### 3. Fazer perguntas sobre o projeto

```
User> consegue me dizer do que se trata esse projeto ?
```

## Sobrescrever o Prompt Padrão

Se você quiser usar um prompt diferente do padrão, pode sobrescrever usando a variável de ambiente:

```bash
export XODEX_SYSTEM_PROMPT="Seu prompt personalizado aqui"
xodex
```

## Exemplos de Prompts Personalizados

### Para Análise de Código
```bash
export XODEX_SYSTEM_PROMPT="Você é um especialista em análise de código. Analise o código fornecido e identifique padrões, problemas potenciais, e sugestões de melhoria."
```

### Para Documentação
```bash
export XODEX_SYSTEM_PROMPT="Você é um especialista em documentação técnica. Ajude a criar documentação clara e completa para o projeto."
```

### Para Debugging
```bash
export XODEX_SYSTEM_PROMPT="Você é um especialista em debugging. Ajude a identificar e resolver problemas no código."
```

### Para Arquitetura
```bash
export XODEX_SYSTEM_PROMPT="Você é um arquiteto de software. Analise a arquitetura do projeto e sugira melhorias estruturais."
```

## Configuração Permanente

Para definir um prompt personalizado permanentemente, adicione ao seu `~/.bashrc` ou `~/.zshrc`:

```bash
echo 'export XODEX_SYSTEM_PROMPT="Seu prompt personalizado aqui"' >> ~/.bashrc
source ~/.bashrc
```

## Contexto do Projeto

O Xodex automaticamente inclui arquivos relevantes do projeto no contexto, incluindo:
- README.md
- package.json / pyproject.toml
- Arquivos de código fonte (src/**/*.py, src/**/*.ts, etc.)
- Arquivos de configuração (*.json, *.yaml, *.yml, etc.)
- Dockerfile e docker-compose

Você pode personalizar quais arquivos incluir usando a variável `CONTEXT_GLOBS`:

```bash
export CONTEXT_GLOBS="*.md,src/**/*.py,*.json"
```

## Modos de Operação

- **Modo Normal**: Fornece orientações e sugestões
- **Modo Agente**: Pode aplicar alterações diretamente nos arquivos
- **Modo Ask**: Responde apenas perguntas específicas

Use `/agent` para ativar o modo agente e `/ask` para perguntas rápidas.
