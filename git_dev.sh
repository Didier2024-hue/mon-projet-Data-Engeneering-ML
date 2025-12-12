#!/bin/bash
set -euo pipefail

# =============================================================================
# GIT DEV - Script de déploiement pour la branche dev
# Version NON-INTERACTIVE pour usage quotidien
# =============================================================================

# --- Configuration des couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Configuration des options ---
AUTO_ADD_NEW_FILES=false  # true: ajoute nouveaux fichiers, false: seulement modifiés
SKIP_PUSH_ON_NO_CHANGES=true
MAX_RETRIES=3
SKIP_LARGE_FILES_CHECK=true  # Ignore la vérification des gros fichiers

# --- Fonctions de logging ---
log_info() { echo -e "${BLUE}ℹ️ $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }

# --- Fonction de vérification des prérequis ---
check_prerequisites() {
    log_info "Vérification des prérequis..."
    
    # Vérifier qu'on est dans un dépôt Git
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Ce répertoire n'est pas un dépôt Git"
        exit 1
    fi
    
    # Vérifier la connexion au remote (mode silencieux)
    if ! git ls-remote origin > /dev/null 2>&1; then
        log_warning "Remote 'origin' non accessible - mode local seulement"
    fi
    
    return 0
}

# --- Fonction de changement de branche ---
switch_to_dev() {
    log_info "Passage sur la branche dev..."
    
    local current_branch=$(git branch --show-current)
    if [ "$current_branch" = "dev" ]; then
        log_info "Déjà sur la branche dev"
        return 0
    fi
    
    # Vérifier si la branche dev existe localement
    if git show-ref --verify --quiet refs/heads/dev; then
        log_info "Changement vers la branche dev existante"
        git switch dev 2>/dev/null || {
            log_warning "Changement vers dev échoué, reste sur $current_branch"
            return 1
        }
    else
        log_info "Création de la branche dev depuis origin/dev"
        git checkout -b dev origin/dev 2>/dev/null || {
            log_info "Création de la branche dev depuis main/master"
            git checkout -b dev 2>/dev/null
        }
    fi
    
    return 0
}

# --- Fonction de mise à jour depuis le remote ---
update_from_remote() {
    log_info "Mise à jour depuis origin/dev..."
    
    if ! git fetch origin dev 2>/dev/null; then
        log_warning "Fetch depuis origin/dev échoué - continuation en mode local"
        return 0
    fi
    
    local local_commit=$(git rev-parse dev 2>/dev/null || echo "")
    local remote_commit=$(git rev-parse origin/dev 2>/dev/null || echo "")
    
    if [ -z "$local_commit" ] || [ -z "$remote_commit" ]; then
        return 0
    fi
    
    if [ "$local_commit" = "$remote_commit" ]; then
        log_success "Branche dev déjà à jour"
        return 0
    fi
    
    log_info "Tentative de mise à jour fast-forward..."
    if git merge --ff-only origin/dev 2>/dev/null; then
        log_success "Mise à jour fast-forward réussie"
    else
        log_warning "Fast-forward impossible - merge récursif"
        git merge -X theirs origin/dev -m "Merge origin/dev" 2>/dev/null || {
            log_warning "Merge échoué - continuation avec état local"
            git merge --abort 2>/dev/null || true
        }
    fi
    
    return 0
}

# --- Fonction d'analyse des fichiers modifiés ---
analyze_changes() {
    log_info "Analyse des modifications en cours..."
    
    local modified_count=$(git status --porcelain | grep -E '^ M' | wc -l)
    local deleted_count=$(git status --porcelain | grep -E '^ D' | wc -l)
    local untracked_count=$(git status --porcelain | grep -E '^\?\?' | wc -l)
    
    echo -e "\n${BLUE}📈 Résumé des changements :${NC}"
    echo "  Modifiés: $modified_count fichiers"
    echo "  Supprimés: $deleted_count fichiers" 
    echo "  Non suivis: $untracked_count fichiers"
    
    # Vérifier les fichiers volumineux (optionnel)
    if [ "$SKIP_LARGE_FILES_CHECK" = false ]; then
        echo -e "\n${BLUE}⚖️  Vérification des fichiers >100 Mo :${NC}"
        local large_files=$(find . -type f -size +100M ! -path "./.git/*" 2>/dev/null | head -5)
        if [ -n "$large_files" ]; then
            echo "$large_files" | while read file; do
                local size=$(du -h "$file" 2>/dev/null | cut -f1 || echo "?")
                log_warning "Fichier volumineux: $file ($size)"
            done
        fi
    fi
    
    # Si pas de changements, on peut s'arrêter ici
    if [ $modified_count -eq 0 ] && [ $deleted_count -eq 0 ] && [ $untracked_count -eq 0 ]; then
        log_success "Aucune modification détectée"
        return 1
    fi
    
    return 0
}

# --- Fonction d'ajout sécurisé des fichiers ---
safe_add_files() {
    log_info "Ajout sécurisé des fichiers..."
    
    if [ "$AUTO_ADD_NEW_FILES" = true ]; then
        log_info "Mode: Ajout de TOUS les fichiers (modifiés et nouveaux)"
        git add -A 2>/dev/null || {
            # Fallback si -A échoue
            git add -u 2>/dev/null
            git add . 2>/dev/null || true
        }
    else
        log_info "Mode: Ajout seulement des fichiers modifiés/supprimés"
        git add -u 2>/dev/null || true
    fi
    
    # Vérifier si quelque chose a été ajouté
    if git diff --cached --quiet 2>/dev/null; then
        log_warning "Aucun fichier à ajouter après git add"
        return 1
    fi
    
    local staged_count=$(git diff --cached --name-only | wc -l)
    log_success "$staged_count fichiers ajoutés au staging"
    
    return 0
}

# --- Fonction de création du commit ---
create_commit() {
    local commit_msg="${1:-"MAJ dev $(date '+%Y-%m-%d %H:%M:%S')"}"
    
    log_info "Création du commit..."
    
    if git diff --cached --quiet 2>/dev/null; then
        log_warning "Aucune modification à committer"
        return 1
    fi
    
    # Commit avec message par défaut si non fourni
    if git commit -m "$commit_msg" 2>/dev/null; then
        log_success "Commit créé: $commit_msg"
        return 0
    else
        log_error "Échec de la création du commit"
        return 1
    fi
}

# --- Fonction de push sécurisé ---
safe_push() {
    log_info "Push vers origin/dev..."
    
    # Vérifier si on peut pousser
    if ! git ls-remote origin > /dev/null 2>&1; then
        log_warning "Pas de remote 'origin' - skip push"
        return 0
    fi
    
    local retry_count=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        if git push origin dev 2>/dev/null; then
            log_success "Push réussi vers origin/dev"
            return 0
        else
            retry_count=$((retry_count + 1))
            if [ $retry_count -lt $MAX_RETRIES ]; then
                log_warning "Échec push (tentative $retry_count/$MAX_RETRIES) - nouvelle tentative..."
                sleep 2
            else
                log_warning "Échec final du push après $MAX_RETRIES tentatives"
                log_info "Le commit reste en local"
                return 1
            fi
        fi
    done
    
    return 1
}

# --- Fonction principale ---
main() {
    local commit_message="${1:-""}"
    
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}🚀 GIT DEV - Déploiement automatique (NON-INTERACTIF)${NC}"
    echo -e "${BLUE}================================================================${NC}"
    
    # Obtenir le chemin racine du dépôt
    REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")
    cd "$REPO_ROOT"
    log_info "Dépôt: $REPO_ROOT"
    log_info "Options: AUTO_ADD_NEW_FILES=$AUTO_ADD_NEW_FILES"
    
    # Workflow principal avec gestion d'erreurs douce
    check_prerequisites || exit 1
    
    switch_to_dev || {
        log_warning "Continue sur la branche actuelle"
    }
    
    update_from_remote
    
    if ! analyze_changes; then
        if [ "$SKIP_PUSH_ON_NO_CHANGES" = true ]; then
            log_success "Aucun changement - script terminé"
            exit 0
        fi
    fi
    
    if safe_add_files; then
        # Message de commit par défaut si non fourni
        if [ -z "$commit_message" ]; then
            commit_message="Auto-commit: $(date '+%Y-%m-%d %H:%M:%S')"
            
            # Ajouter un préfixe basé sur les changements
            local changed_files=$(git diff --cached --name-only | head -3 | tr '\n' ', ' | sed 's/, $//')
            if [ -n "$changed_files" ]; then
                commit_message="Update: $changed_files"
            fi
        fi
        
        if create_commit "$commit_message"; then
            safe_push
        fi
    else
        log_warning "Aucun fichier à committer"
    fi
    
    echo -e "${GREEN}================================================================${NC}"
    echo -e "${GREEN}✨ Script terminé${NC}"
    echo -e "${GREEN}================================================================${NC}"
}

# --- Gestion des arguments ---
# Usage: ./git_dev.sh [message_de_commit] [--add-new] [--skip-push]
while [[ $# -gt 0 ]]; do
    case $1 in
        --add-new)
            AUTO_ADD_NEW_FILES=true
            shift
            ;;
        --skip-push)
            SKIP_PUSH_ON_NO_CHANGES=true
            shift
            ;;
        --help)
            echo "Usage: $0 [commit_message] [options]"
            echo "Options:"
            echo "  --add-new     : Ajoute les nouveaux fichiers (sinon seulement modifiés)"
            echo "  --skip-push   : Ne pas pousser si pas de changements"
            echo "  --help        : Affiche cette aide"
            exit 0
            ;;
        *)
            # Premier argument non-optionnel = message de commit
            if [[ -z "$COMMIT_MSG" ]]; then
                COMMIT_MSG="$1"
            fi
            shift
            ;;
    esac
done

# --- Exécution ---
trap 'log_error "Script interrompu"; exit 1' INT TERM
main "${COMMIT_MSG:-}"