#!/bin/bash
set -euo pipefail

echo " Lancement des tests PyTest..."

pytest -q --disable-warnings --maxfail=1

echo " Tests OK"

