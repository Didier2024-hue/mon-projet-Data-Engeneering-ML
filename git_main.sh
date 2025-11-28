#!/bin/bash
set -euo pipefail

# =============================================
#   DEPLOIEMENT DEV → MAIN  (Version Sécurisée)
#   Écrase complètement main avec l’état de dev
# =============================================

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()    { echo -e "${BLUE}ℹ️ $1${NC}"; }
ok()     { echo -e "${GREEN}✅ $1${NC}"; }
warn()   { echo -e "${YELLOW}⚠️ $1${NC}"; }
error()  { echo -e "${RED}❌ $1${NC}"; exit 1; }

# -------------------------------------------------
# 1️⃣ Vérifier que nous sommes bien sur dev
# -------------------------------------------------
log "Vérification de la branche active..."

branch=$(git branch --show-current)

if [ "$branch" != "dev" ]; then
    error "Vous devez être sur la branche DEV pour lancer ce script (actuel: $branch)"
fi

ok "Vous êtes bien sur la branche dev"


# -------------------------------------------------
# 2️⃣ Vérifier qu’il n’y a rien à committer sur dev
# -------------------------------------------------
log "Vérification du working directory sur dev..."

if ! git diff --quiet || ! git diff --cached --quiet; then
    error "Des changements non commités existent sur DEV. Committez ou stashez avant."
fi

ok "Aucun changement en attente sur dev"


# -------------------------------------------------
# 3️⃣ Vérifier qu'il n’y a rien à committer dans main
#    (si elle existe localement)
# -------------------------------------------------
if git show-ref --verify --quiet refs/heads/main; then
    log "La branche main existe localement. Vérification…"

    # On se met sur main en lecture seule (sans y rester)
    git checkout main >/dev/null 2>&1 || error "Impossible de basculer sur main"

    if ! git diff --quiet || ! git diff --cached --quiet; then
        git checkout dev >/dev/null
        error "Des changements non commités existent sur MAIN. Résolvez-les avant sync."
    fi

    git checkout dev >/dev/null
    ok "Aucun changement en attente sur main"
else
    warn "La branche main n’existe pas encore localement — ce n’est pas un problème."
fi


# -------------------------------------------------
# 4️⃣ Suppression propre de main
# -------------------------------------------------
log "Suppression de la branche main locale (si existante)..."
git branch -D main 2>/dev/null || true


# -------------------------------------------------
# 5️⃣ Création de main depuis dev
# -------------------------------------------------
log "Création de la branche main depuis dev..."
git checkout -b main

msg="Sync dev → main ($(date '+%Y-%m-%d %H:%M:%S'))"
git commit --allow-empty -m "$msg"

ok "Branche main créée et commit de sync ajouté"


# -------------------------------------------------
# 6️⃣ Push forcé vers origin/main
# -------------------------------------------------
log "Push forcé vers origin/main..."
git push origin main --force

ok "Main est maintenant IDENTIQUE à dev (synchronisation réussie)"


# -------------------------------------------------
# 7️⃣ Retour sur dev
# -------------------------------------------------
git checkout dev
ok "Retour sur dev"


echo -e "${GREEN}🎉 Synchronisation DEV → MAIN effectuée avec succès !${NC}"
