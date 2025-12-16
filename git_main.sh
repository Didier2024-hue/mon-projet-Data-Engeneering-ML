#!/bin/bash
set -euo pipefail

# =====================================================
#   GIT MAIN — Synchronisation DEV → MAIN
#   À lancer UNIQUEMENT depuis la branche dev
# =====================================================

# --- Couleurs ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()   { echo -e "${BLUE}ℹ️  $1${NC}"; }
ok()    { echo -e "${GREEN}✅ $1${NC}"; }
warn()  { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}🚀 GIT MAIN - Déploiement PRODUCTION${NC}"
echo -e "${BLUE}================================================================${NC}"

# ---------------------------------------------------
# 🔒 Protection de branche (CLAIRE ET UNIQUE)
# ---------------------------------------------------
current_branch=$(git branch --show-current)

if [ "$current_branch" = "main" ]; then
    error "Ce script NE DOIT PAS être lancé depuis 'main'. Lance-le depuis 'dev'."
fi

if [ "$current_branch" != "dev" ]; then
    error "Vous devez être sur DEV pour lancer ce script (actuel: $current_branch)"
fi

ok "Branche dev confirmée"

# ---------------------------------------------------
# Vérification état propre
# ---------------------------------------------------
log "Vérification des changements non commités…"
if ! git diff --quiet || ! git diff --cached --quiet; then
    error "DEV contient des changements non commités. Committez ou stash avant."
fi
ok "DEV propre"

# ---------------------------------------------------
# Synchronisation main ← dev
# ---------------------------------------------------
log "Synchronisation de main avec dev…"

if git show-ref --verify --quiet refs/heads/main; then
    git checkout main
else
    git checkout -b main
fi

git reset --hard dev
ok "Main alignée sur dev"

# ---------------------------------------------------
# Commit de synchronisation
# ---------------------------------------------------
sync_msg="Sync dev → main ($(date '+%Y-%m-%d %H:%M:%S'))"
git commit --allow-empty -m "$sync_msg"
ok "Commit de sync créé"

# ---------------------------------------------------
# Push vers remotes
# ---------------------------------------------------
log "Push vers GitHub (origin/main)…"
git push origin main --force
ok "GitHub OK"

log "Push vers GitLab (gitlab/main)…"
git push gitlab main --force
ok "GitLab OK"

# ---------------------------------------------------
# Retour sur dev
# ---------------------------------------------------
git checkout dev
ok "Retour sur dev effectué"

echo -e "${GREEN}🎉 Synchronisation DEV → MAIN réussie${NC}"
