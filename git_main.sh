#!/bin/bash
# =====================================================
# 🚀 Script de synchronisation : DEV → MAIN
# =====================================================
# ⚠️ ÉCRASE entièrement la branche MAIN distante.
# Utiliser uniquement lorsque DEV est stable.
# =====================================================

set -e  # Stoppe le script en cas d'erreur

# Vérification : on doit être sur dev
current_branch=$(git rev-parse --abbrev-ref HEAD)
if [ "$current_branch" != "dev" ]; then
  echo "❌ Tu n'es pas sur la branche 'dev'."
  echo "➡️  Fais : git checkout dev"
  exit 1
fi

# Vérifier l'état du workspace
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "⚠️ Il reste des changements non commités."
  echo "➡️  Commit ou stash avant de synchroniser."
  exit 1
fi

# Message de commit (optionnel – traçabilité)
msg=${1:-"Sync dev → main ($(date '+%Y-%m-%d %H:%M:%S'))"}

echo "🔄 Synchronisation DEV → MAIN"
echo "ℹ️  Message : $msg"

# Supprimer la branche main locale si elle existe
git branch -D main 2>/dev/null || true

# Créer main depuis dev
git checkout -b main

# Créer un commit de traçabilité (optionnel)
git commit --allow-empty -m "$msg"

# Push forcé
echo "🚀 Push forcé vers remote/main..."
git push origin main --force

# Retour sur dev
git checkout dev

echo "✅ Synchronisation DEV → MAIN terminée"