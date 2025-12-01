#!/bin/bash
set -euo pipefail

# =====================================================
#   SYNC DEV → MAIN  (GitHub + GitLab)
#   Écrase complètement main avec l'état de dev
#   Aucun merge, aucun rebase, jamais de conflits
# =====================================================

# --- Couleurs ---
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()    { echo -e "${BLUE}ℹ️  $1${NC}"; }
ok()     { echo -e "${GREEN}✅ $1${NC}"; }
warn()   { echo -e "${YELLOW}⚠️  $1${NC}"; }
error()  { echo -e "${RED}❌ $1${NC}"; exit 1; }

# ---------------------------------------------------
# 1️⃣ Vérification branche active
# ---------------------------------------------------
log "Vérification de la branche active…"

current_branch=$(git branch --show-current)
if [[ "$current_branch" != "dev" ]]; then
    error "Vous devez être sur DEV pour lancer ce script (actuel: $current_branch)"
fi

ok "Branche dev active"

# ---------------------------------------------------
# 2️⃣ Vérifier qu'il n'y a rien à committer
# ---------------------------------------------------
log "Vérification des modifications non committées…"

if ! git diff --quiet || ! git diff --cached --quiet; then
    error "Des changements non commités existent dans DEV. Committez ou stash avant."
fi

ok "Aucune modification en attente"

# ---------------------------------------------------
# 3️⃣ Suppression propre de main (si existe)
# ---------------------------------------------------
log "Suppression locale de main (si existante)…"
git branch -D main 2>/dev/null || true

# ---------------------------------------------------
# 4️⃣ Création de main depuis dev
# ---------------------------------------------------
log "Création de la branche main basée sur dev…"
git checkout -b main

sync_msg="Sync dev → main ($(date '+%Y-%m-%d %H:%M:%S'))"
git commit --allow-empty -m "$sync_msg"

ok "Branche main créée"

# ---------------------------------------------------
# 5️⃣ Push forcé vers GitHub (origin)
# ---------------------------------------------------
log "Push forcé vers GitHub (origin/main)…"
git push origin main --force

ok "GitHub main mis à jour"

# ---------------------------------------------------
# 6️⃣ Push forcé vers GitLab (gitlab)
# ---------------------------------------------------
log "Push forcé vers GitLab (gitlab/main)…"
git push gitlab main --force

ok "GitLab main mis à jour"

# ---------------------------------------------------
# 7️⃣ Retour sur dev
# ---------------------------------------------------
git checkout dev
ok "Retour sur DEV effectué"

echo -e "${GREEN}🎉 Synchronisation DEV → MAIN réussie sur GitHub + GitLab${NC}"