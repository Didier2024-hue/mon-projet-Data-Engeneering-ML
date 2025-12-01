#!/bin/bash
set -euo pipefail

echo "🔍 Lint Python — API uniquement"

flake8 \
  api/ \
  api/scripts/app_api/ \
  --max-line-length=200 \
  --ignore=E302,E305,E402,E501,W293,W391,F401,F841,E704,E241,W291,E226,E303

echo "✅ Lint API OK"