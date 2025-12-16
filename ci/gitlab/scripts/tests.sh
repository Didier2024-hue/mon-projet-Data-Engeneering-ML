#!/bin/bash
set -euo pipefail

echo "🧪 Lancement des tests API (pytest)"
echo "📦 Conteneur cible : fastapi-cde"

# Vérifie que le conteneur est bien en cours d'exécution
if ! docker ps --format '{{.Names}}' | grep -q "^fastapi-cde$"; then
    echo "❌ Le conteneur fastapi-cde n'est pas démarré."
    echo "👉 Lance-le manuellement avant d'exécuter ce job."
    exit 1
fi

# Exécution des tests dans le conteneur API
docker exec fastapi-cde pytest -v --disable-warnings --maxfail=1

echo "✅ Tests API terminés avec succès !"
