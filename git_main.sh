#!/bin/bash
set -euo pipefail

# --- 0) Aller à la racine du dépôt ---
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || {
  echo "❌ Ce script doit être lancé DANS un dépôt git."; exit 1;
})
cd "$REPO_ROOT"
echo "📂 Repo : $REPO_ROOT"

# --- 1) Vérifier que l'arbre de travail est propre ---
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "❌ Le dépôt n'est pas propre (modifs non committées)."
  echo "   Fais ton ./git_dev.sh (ou un commit/stash manuel) AVANT de lancer git_main.sh."
  exit 1
fi

# --- 2) Récupérer les dernières infos du remote ---
echo "🌐 Fetch des infos du remote…"
git fetch origin

# --- 3) S'assurer que dev est à jour ---
echo "🔍 Mise à jour de la branche dev…"
if git show-ref --verify --quiet refs/heads/dev; then
    git switch dev
else
    git checkout -b dev origin/dev
fi

if ! git pull --ff-only origin dev 2>/dev/null; then
    echo "⚠️ La branche dev diverge de origin/dev."
    echo "   Fais un 'git pull --rebase origin dev' ou 'git merge origin/dev' manuellement."
    exit 1
fi

# --- 4) Passer sur main et la mettre à jour ---
echo "🔍 Passage sur main…"
if git show-ref --verify --quiet refs/heads/main; then
    git switch main
else
    git checkout -b main origin/main
fi

echo "🔄 Mise à jour de main depuis origin/main…"
if ! git pull --ff-only origin main 2>/dev/null; then
    echo "⚠️ La branche main diverge de origin/main."
    echo "   Corrige manuellement (merge ou rebase) puis relance ce script."
    exit 1
fi

# --- 5) Merge dev -> main ---
echo "🔀 Merge dev -> main…"
if ! git merge --no-ff dev -m "Merge dev into main"; then
    echo "❌ Conflits de merge."
    echo "   Résous les conflits, fais 'git add …', 'git commit', puis 'git push origin main'."
    exit 1
fi

# --- 6) Push main ---
echo "⬆️ Push main vers origin/main…"
git push origin main

echo "✅ git_main.sh terminé : main contient maintenant le code de dev."
