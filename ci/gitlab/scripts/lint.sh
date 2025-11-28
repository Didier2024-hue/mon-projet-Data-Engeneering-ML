#!/bin/bash
set -euo pipefail

echo "🔍 Lint Python ciblé (API + Streamlit + app_api)..."

flake8 \
  api/ \
  scripts/app/ \
  api/scripts/app_api/ \
  --max-line-length=120 \
  --exclude="__pycache__,*.venv" 

echo "✅ Lint OK (zones critiques du projet)"

