#!/bin/bash
# =====================================================
# 🚀 Script de synchronisation : DEV → MAIN
# =====================================================
# ⚠️ Ce script écrase complètement la branche MAIN distante
# avec le contenu actuel de la branche DEV.
# Utiliser uniquement si DEV est stable.

set -e  # Stoppe le script en cas d'erreur

# Vérification de la branche actuelle
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" != "dev" ]; then
  echo "❌ Tu n'es pas sur la branche 'dev'."
  echo "➡️  Fais 'git checkout dev' avant de lancer ce script."
  exit 1
fi

# Vérifie s'il y a des changements non commités
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "⚠️  Des modifications locales non commités ont été détectées."
  echo "   -> Fais un commit propre avant d'exécuter la synchro."
  exit 1
fi

# Message de commit pour traçabilité (si besoin)
if [ -z "$1" ]; then
  msg="Sync dev -> main ($(date '+%Y-%m-%d %H:%M:%S'))"
else
  msg="$1"
fi

# Supprimer l'ancienne branche main locale (si elle existe)
git branch -D main 2>/dev/null || true

# Créer main à partir de dev
git checkout -b main

# Pousser en forçant main à refléter dev
echo "🚀 Synchronisation en cours (dev → main)..."
git push origin main --force

# Revenir sur dev
git checkout dev

echo "✅ Synchronisation terminée avec succès !"
