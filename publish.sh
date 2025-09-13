#!/bin/bash

# Script para publicar nova versão do xodex-cli

set -e

echo "🚀 Publicando nova versão do xodex-cli..."

# Verificar se a versão foi atualizada
CURRENT_VERSION=$(grep 'version = ' pyproject.toml | cut -d'"' -f2)
echo "📦 Versão atual: $CURRENT_VERSION"

# Limpar builds anteriores
echo "🧹 Limpando builds anteriores..."
rm -rf dist/ build/ *.egg-info/

# Construir nova versão
echo "🔨 Construindo pacote..."
export PATH="$HOME/.local/bin:$PATH"
python3 -m build

# Verificar o pacote
echo "✅ Verificando pacote..."
twine check dist/*

# Publicar no PyPI
echo "📤 Publicando no PyPI..."
twine upload dist/*

echo "🎉 Versão $CURRENT_VERSION publicada com sucesso!"
echo "💡 Agora você pode testar: pip install xodex-cli==$CURRENT_VERSION"
