#!/usr/bin/env bash
set -euo pipefail

# Uso: ./release.sh v0.1.0
VERSION="${1:-}"

if [[ -z "${VERSION}" ]]; then
  echo "Uso: $0 vX.Y.Z"
  exit 1
fi

command -v git >/dev/null || { echo "git não encontrado"; exit 1; }
command -v gh  >/dev/null || { echo "GitHub CLI (gh) não encontrado"; exit 1; }

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "${BRANCH}" != "main" && "${BRANCH}" != "master" ]]; then
  echo "⚠️  Você está na branch '${BRANCH}'. Continuar? [y/N]"
  read -r ans; [[ "${ans}" == "y" || "${ans}" == "Y" ]] || exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "❌ Há mudanças não commitadas. Faça commit/stash antes."
  exit 1
fi

# Atualiza versão no pyproject.toml (se existir linha version = "...")
if [[ -f "pyproject.toml" ]]; then
  echo "🔧 Atualizando versão no pyproject.toml -> ${VERSION}"
  # sed compatível com macOS e Linux
  sed -i.bak -E "s/^(version\s*=\s*\")([^\"]+)(\")/\1${VERSION#v}\3/" pyproject.toml || true
  rm -f pyproject.toml.bak
  if ! git diff --quiet; then
    git add pyproject.toml
    git commit -m "chore(release): ${VERSION}"
  else
    echo "ℹ️  pyproject.toml já estava com ${VERSION#v} (ou sem campo version)."
  fi
fi

echo "🏷️  Criando tag ${VERSION}…"
git tag -a "${VERSION}" -m "Release ${VERSION}"
git push origin "${BRANCH}"
git push origin "${VERSION}"

echo
echo "🚀 Tag enviada. O workflow 'Release Binaries' (GitHub Actions) deve iniciar e anexar os binários."
echo "   Acompanhe: gh run list --workflow 'Release Binaries' --branch ${BRANCH}"
echo
echo "🔗 Releases: https://github.com/thiagovt-dev/xodex/releases"
echo
cat <<'EOSHA'
ℹ️  Após os binários aparecerem, obtenha os SHA256 (p/ Homebrew):
# Linux
curl -L -o xodex-linux-amd64 https://github.com/thiagovt-dev/xodex/releases/latest/download/xodex-linux-amd64
shasum -a 256 xodex-linux-amd64

# macOS Intel
curl -L -o xodex-macos-x64 https://github.com/thiagovt-dev/xodex/releases/latest/download/xodex-macos-x64
shasum -a 256 xodex-macos-x64

# macOS ARM
curl -L -o xodex-macos-arm64 https://github.com/thiagovt-dev/xodex/releases/latest/download/xodex-macos-arm64
shasum -a 256 xodex-macos-arm64
EOSHA
