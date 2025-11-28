#!/bin/bash
set -euo pipefail

echo " Lint Python avec flake8..."

flake8 \
  --exclude=".venv,.git,data,mlruns,docker,ci,notebooks" \
  --max-line-length=120 \
  .

echo "Lint OK"

