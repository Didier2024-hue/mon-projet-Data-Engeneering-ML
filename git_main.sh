#!/bin/bash
set -euo pipefail

# =====================================================
#   GIT MAIN — Le bouton de déploiement conscient
#   Déclenchement MANUEL et CONTRÔLÉ de la CI/CD
# =====================================================

# --- Couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

log()   { echo -e "${BLUE}ℹ️  $1${NC}"; }
ok()    { echo -e "${GREEN}✅ $1${NC}"; }
warn()  { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

echo -e "${BLUE}================================================================${NC}"
echo -e "${MAGENTA}🚀 BOUTON DE DÉPLOIEMENT - Déclenchement CI/CD${NC}"
echo -e "${BLUE}================================================================${NC}"

# ---------------------------------------------------
# 🔒 SCÉNARIO 1 : Vérification de branche
# ---------------------------------------------------
current_branch=$(git branch --show-current)

if [ "$current_branch" = "main" ]; then
    error "DANGER : Vous êtes sur 'main' !\nCe script doit être lancé depuis 'dev'."
fi

if [ "$current_branch" != "dev" ]; then
    error "ACTION REQUISE : Placez-vous sur 'dev' (actuel: $current_branch)"
fi
ok "✓ Branche 'dev' confirmée"

# ---------------------------------------------------
# 🔒 SCÉNARIO 2 : État propre
# ---------------------------------------------------
log "Vérification de l'état du répertoire…"
if ! git diff --quiet || ! git diff --cached --quiet; then
    error "ATTENTION : Modifications non commitées détectées !\nCommitez ou stash avant de déployer."
fi
ok "✓ Aucune modification en attente"

# ---------------------------------------------------
# 🔒 Vérification supplémentaire : Conflits potentiels
# ---------------------------------------------------
log "Vérification des divergences avec GitLab…"
git fetch gitlab --quiet

# Vérifier si main sur GitLab est en avance
if git log dev..gitlab/main --oneline 2>/dev/null | grep -q .; then
    warn "ALERTE : 'main' sur GitLab contient des commits absents de 'dev' !"
    echo -e "${YELLOW}Commits sur gitlab/main mais pas dans dev :${NC}"
    git log dev..gitlab/main --oneline
    echo -e "\n${RED}ACTION : Fusionnez manuellement ces changements avant de déployer.${NC}"
    exit 1
fi
ok "✓ Aucun conflit détecté"

# ---------------------------------------------------
# 🎯 SCÉNARIO 3 : Tout va bien → Déploiement
# ---------------------------------------------------
echo -e "${GREEN}===============================================================${NC}"
echo -e "${GREEN}                DÉPLOIEMENT AUTORISÉ                          ${NC}"
echo -e "${GREEN}===============================================================${NC}"

log "📤 Synchronisation dev → main en cours…"

# Sauvegarde du SHA actuel pour traçabilité
dev_sha=$(git rev-parse --short dev)
log "SHA actuel de dev: $dev_sha"

# Basculer sur main et appliquer les changements
git checkout main
ok "✓ Basculé sur 'main'"

# Option A : Merge propre (recommandé pour l'historique)
git merge --no-ff dev -m "🚀 Déploiement PROD [SHA: $dev_sha] - $(date '+%Y-%m-%d %H:%M:%S')"
ok "✓ Fusion propre effectuée"

# Option B : Reset hard (si vous préférez vraiment)
# git reset --hard dev
# git commit --allow-empty -m "🔄 Sync dev → main [SHA: $dev_sha] - $(date '+%Y-%m-%d %H:%M:%S')"

# ---------------------------------------------------
# 📡 Push et déclenchement CI/CD
# ---------------------------------------------------
log "🔄 Envoi vers GitHub (backup)…"
if git push origin main; then
    ok "✓ GitHub synchronisé"
else
    warn "GitHub non disponible (peut-être pas configuré)"
fi

log "🚀 Déclenchement CI/CD GitLab…"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}⚠️  POINT DE NON RETOUR ⚠️${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Confirmation utilisateur
read -p "Confirmez-vous le déclenchement de la CI/CD sur GitLab ? (oui/non): " confirm
if [[ $confirm != "oui" ]]; then
    echo -e "${YELLOW}⚠️  Déploiement annulé par l'utilisateur${NC}"
    git checkout dev
    exit 0
fi

if git push gitlab main; then
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}🎯 DÉPLOIEMENT RÉUSSI !${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    ok "✓ GitLab CI/CD déclenchée !"
    echo -e "${CYAN}📊 Vérifiez l'état sur : https://gitlab.com/kiemberaid/cde/pipelines${NC}"
else
    error "Échec du push vers GitLab"
fi

# ---------------------------------------------------
# 🔄 Retour à la normale
# ---------------------------------------------------
git checkout dev
ok "✓ Retour sur 'dev'"

# ---------------------------------------------------
# 📋 Résumé du déploiement
# ---------------------------------------------------
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}            RÉSUMÉ DU DÉPLOIEMENT        ${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}• SHA déployé : $dev_sha${NC}"
echo -e "${CYAN}• Date/Heure  : $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo -e "${CYAN}• Pipeline    : https://gitlab.com/kiemberaid/cde/pipelines${NC}"
echo -e "${CYAN}• Jobs        : https://gitlab.com/kiemberaid/cde/-/jobs${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${MAGENTA}🎉 Déploiement terminé avec succès !${NC}"
echo -e "${BLUE}ℹ️  La pipeline GitLab CI/CD est maintenant en cours d'exécution.${NC}"