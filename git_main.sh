#!/bin/bash
set -euo pipefail

# =============================================================================
# GIT MAIN - Script de déploiement PRODUCTION
# Merge dev → main avec vérifications de sécurité
# =============================================================================

# --- Configuration des couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# --- Configuration ---
GITHUB_REPO="origin"
GITLAB_REPO="gitlab"
DRY_RUN=false
FORCE_MODE=false

# --- Fonctions de logging ---
log() { echo -e "${BLUE}ℹ️ $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }
step() { echo -e "${CYAN}👉 $1${NC}"; }
ci() { echo -e "${MAGENTA}🚀 $1${NC}"; }

# --- Fonction d'affichage d'en-tête ---
show_header() {
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}🚀 GIT MAIN - Déploiement PRODUCTION${NC}"
    echo -e "${BLUE}================================================================${NC}"
}

# --- Vérification : Branche actuelle ---
check_current_branch() {
    step "Vérification de la branche actuelle..."
    
    local current_branch=$(git branch --show-current)
    
    if [ "$current_branch" != "main" ]; then
        error "Tu dois être sur 'main' pour déployer !"
        log "Tu es sur: $current_branch"
        log "Pour déployer, fais d'abord: git switch main"
        exit 1
    fi
    
    success "Branche OK: $current_branch"
}

# --- Vérification : État du working directory ---
check_working_directory() {
    step "Vérification de l'état du working directory..."
    
    if ! git diff --quiet; then
        warning "Hé ! Tu as des modifications non commitées !"
        log "Fichiers modifiés :"
        git status --short
        
        if [ "$FORCE_MODE" = false ]; then
            log "Soit :"
            log "  1. Committe-les : git add . && git commit -m '...'"
            log "  2. Stash-les : git stash"
            log "  3. Force le déploiement : ./git_main.sh --force"
            exit 1
        else
            warning "Mode FORCE activé - ignoring uncommitted changes"
        fi
    fi
    
    success "Working directory propre"
}

# --- Vérification : Différences dev → main ---
show_diff_summary() {
    step "Analyse des changements à déployer..."
    
    if ! git show-ref --verify --quiet refs/heads/dev; then
        error "Branche 'dev' n'existe pas localement"
        exit 1
    fi
    
    echo -e "\n${CYAN}📊 Différences dev → main :${NC}"
    
    # Nombre de commits
    local commit_count=$(git log --oneline main..dev | wc -l)
    log "  $commit_count nouveaux commits sur dev"
    
    # Fichiers modifiés
    local changed_files=$(git diff --name-only main dev | wc -l)
    log "  $changed_files fichiers modifiés"
    
    if [ $commit_count -eq 0 ]; then
        warning "Aucun nouveau commit sur dev - rien à déployer"
        if [ "$FORCE_MODE" = false ]; then
            exit 0
        fi
    fi
    
    # Afficher les derniers commits
    echo -e "\n${CYAN}🔍 Derniers commits sur dev :${NC}"
    git log --oneline -5 dev
    
    # Afficher les fichiers modifiés
    if [ $changed_files -lt 20 ]; then
        echo -e "\n${CYAN}📁 Fichiers modifiés :${NC}"
        git diff --name-only main dev
    else
        echo -e "\n${CYAN}📁 Top 10 fichiers modifiés :${NC}"
        git diff --name-only main dev | head -10
        log "  ... et $(($changed_files - 10)) autres"
    fi
}

# --- Confirmation utilisateur (sauf en dry-run ou force) ---
ask_confirmation() {
    if [ "$DRY_RUN" = true ] || [ "$FORCE_MODE" = true ]; then
        return 0
    fi
    
    echo -e "\n${YELLOW}⚠️  CONFIRMATION REQUISE ⚠️${NC}"
    echo "Tu es sur le point de merger dev → main et déclencher la CI/CD."
    echo -n "Continuer ? (oui/NON) : "
    
    read -r response
    if [[ ! "$response" =~ ^[Oo](ui)?$ ]]; then
        warning "Déploiement annulé"
        exit 0
    fi
}

# --- Merge dev → main ---
merge_dev_to_main() {
    step "Merge dev → main..."
    
    if [ "$DRY_RUN" = true ]; then
        log "[DRY RUN] git merge --no-ff dev -m 'Release: $(date)'"
        return 0
    fi
    
    # Merge avec message
    local merge_msg="Release: $(date '+%Y-%m-%d %H:%M:%S')"
    
    if git merge --no-ff dev -m "$merge_msg"; then
        success "Merge réussi"
    else
        error "Merge conflict !"
        log "Résolution manuelle nécessaire :"
        log "  1. Corrige les conflits"
        log "  2. git add ."
        log "  3. git commit"
        exit 1
    fi
}

# --- Push vers les remotes ---
push_to_remotes() {
    step "Push vers les dépôts distants..."
    
    # GitHub
    if git ls-remote "$GITHUB_REPO" > /dev/null 2>&1; then
        ci "Push vers GitHub ($GITHUB_REPO)..."
        if [ "$DRY_RUN" = true ]; then
            log "[DRY RUN] git push $GITHUB_REPO main"
        elif git push "$GITHUB_REPO" main; then
            success "GitHub ✓"
        else
            warning "Push GitHub échoué"
        fi
    else
        log "GitHub remote non configuré"
    fi
    
    # GitLab
    if git ls-remote "$GITLAB_REPO" > /dev/null 2>&1; then
        ci "Push vers GitLab ($GITLAB_REPO)..."
        if [ "$DRY_RUN" = true ]; then
            log "[DRY RUN] git push $GITLAB_REPO main"
        elif git push "$GITLAB_REPO" main; then
            success "GitLab ✓"
        else
            warning "Push GitLab échoué"
        fi
    else
        log "GitLab remote non configuré"
    fi
}

# --- Retour sur dev ---
switch_back_to_dev() {
    step "Retour sur la branche dev..."
    
    if [ "$DRY_RUN" = true ]; then
        log "[DRY RUN] git switch dev"
        return 0
    fi
    
    if git switch dev; then
        success "Retour sur dev ✓"
    else
        warning "Impossible de revenir sur dev"
    fi
}

# --- Fonction principale ---
main() {
    show_header
    
    # Vérifications de sécurité
    check_current_branch
    check_working_directory
    show_diff_summary
    
    # Confirmation
    ask_confirmation
    
    # Déploiement
    merge_dev_to_main
    push_to_remotes
    switch_back_to_dev
    
    # Succès
    echo -e "\n${GREEN}================================================================${NC}"
    echo -e "${GREEN}🎉 DÉPLOIEMENT RÉUSSI !${NC}"
    echo -e "${GREEN}================================================================${NC}"
    ci "La CI/CD est maintenant déclenchée sur main !"
    
    if [ "$DRY_RUN" = false ]; then
        echo -e "\n${CYAN}📈 Status :${NC}"
        git log --oneline -3 --all --graph
    fi
}

# --- Gestion des arguments ---
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE_MODE=true
            shift
            ;;
        --github)
            GITHUB_REPO="$2"
            shift 2
            ;;
        --gitlab)
            GITLAB_REPO="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --dry-run          : Simule sans rien modifier"
            echo "  --force           : Force malgré les warnings"
            echo "  --github <remote> : Remote GitHub (défaut: origin)"
            echo "  --gitlab <remote> : Remote GitLab (défaut: gitlab)"
            echo "  --help            : Affiche cette aide"
            echo ""
            echo "Exemples:"
            echo "  $0                 : Déploiement normal"
            echo "  $0 --dry-run       : Simulation"
            echo "  $0 --force         : Force le déploiement"
            exit 0
            ;;
        *)
            error "Option inconnue: $1"
            echo "Utilisez --help pour l'aide"
            exit 1
            ;;
    esac
done

# --- Exécution ---
trap 'error "Script interrompu"; exit 1' INT TERM

if [ "$DRY_RUN" = true ]; then
    warning "MODE DRY RUN - aucune modification ne sera faite"
fi

if [ "$FORCE_MODE" = true ]; then
    warning "MODE FORCE - ignore les warnings"
fi

main