#!/bin/bash
set -e

echo "🔍 Switch sur 'dev'..."
git checkout dev 2>/dev/null || git checkout -b dev

echo "🧽 Nettoyage léger du cache Git (sans toucher aux fichiers internes)..."
git rm --cached -r data model logs __pycache__ tmp 2>/dev/null || true

echo "⚖️ Recherche fichiers >100 Mo..."
large=$(find data -type f -size +100M 2>/dev/null)

if [ -n "$large" ]; then
    echo "🚫 Fichiers lourds détectés :"
    echo "$large"
    echo "$large" >> .gitignore
    git rm --cached $large 2>/dev/null || true
else
    echo "✅ Aucun fichier lourd."
fi

echo "📦 Ajout des fichiers..."
git add .

msg=${1:-"Update on dev $(date)"}
git commit -m "$msg" || echo "ℹ️ Rien à committer"

echo "⬆️ Push..."
git push origin dev --force

echo "✅ DONE!"