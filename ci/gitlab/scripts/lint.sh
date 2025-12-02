#!/bin/bash
set -euo pipefail

echo "🔍 Lint Python — scripts uniquement (pas l'API)"

# On suppose que le script est lancé depuis la racine du projet (CI_PROJECT_DIR)
SCRIPT_DIR="./scripts"

TARGETS=(
    "$SCRIPT_DIR/app"
    "$SCRIPT_DIR/db"
    "$SCRIPT_DIR/insert"
    "$SCRIPT_DIR/models"
    "$SCRIPT_DIR/preprocess"
    "$SCRIPT_DIR/scraping"
)

echo "📁 Répertoires analysés par flake8 :"
printf '%s\n' "${TARGETS[@]}"

flake8 \
  "${TARGETS[@]}" \
  --max-line-length=200 \
  --ignore=E302,E305,E402,E501,W293,W391,F401,F841,E704,E241,W291,E226,E303

echo "✅ Lint scripts OK"
