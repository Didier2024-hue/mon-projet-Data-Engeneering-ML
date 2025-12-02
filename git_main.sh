#!/bin/bash
set -euo pipefail

# =====================================================
#   SYNC DEV → MAIN  (GitHub + GitLab)
#   
# =====================================================

# --- Couleurs (TES couleurs) ---
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
# 3️⃣ AMÉLIORATION : Sync main avec dev
# ---------------------------------------------------
log "Synchronisation de main avec dev…"

# Solution qui garde l'historique :
if git show-ref --verify --quiet refs/heads/main; then
    # Main existe → on la met à jour
    git checkout main
    git reset --hard dev
else
    # Main n'existe pas → on la crée
    git checkout -b main dev
fi

ok "Main synchronisée avec dev"

# ---------------------------------------------------
# 4️⃣ Création du commit de sync (TON CODE)
# ---------------------------------------------------
log "Création du commit de synchronisation…"
sync_msg="Sync dev → main ($(date '+%Y-%m-%d %H:%M:%S'))"
git commit --allow-empty -m "$sync_msg"
ok "Commit de sync créé"

# ---------------------------------------------------
# 5️⃣ AMÉLIORATION : Push avec --force-with-lease d'abord
# ---------------------------------------------------
log "Push vers GitHub (origin/main)…"
# Essaye d'abord la méthode safe
if git push origin main --force-with-lease 2>/dev/null; then
    ok "GitHub main mis à jour (force-with-lease)"
else
    # Fallback sur --force (comme ton code)
    warn "force-with-lease échoué, utilisation de --force"
    git push origin main --force
    ok "GitHub main mis à jour (force)"
fi

# ---------------------------------------------------
# 6️⃣ Push vers GitLab 
# ---------------------------------------------------
log "Push vers GitLab (gitlab/main)…"
if git push gitlab main --force-with-lease 2>/dev/null; then
    ok "GitLab main mis à jour (force-with-lease)"
else
    warn "force-with-lease échoué, utilisation de --force"
    git push gitlab main --force
    ok "GitLab main mis à jour (force)"
fi

# ---------------------------------------------------
# 7️⃣ Retour sur dev (TON CODE)
# ---------------------------------------------------
git checkout dev
ok "Retour sur DEV effectué"

echo -e "${GREEN}🎉 Synchronisation DEV → MAIN réussie sur GitHub + GitLab${NC}"