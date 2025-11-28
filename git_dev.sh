#!/bin/bash
set -euo pipefail

# =============================================================================
# GIT DEV - Script de déploiement pour la branche dev
# Version sécurisée avec gestion des erreurs et des permissions
# =============================================================================

# --- Configuration des couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    
    # Vérifier la connexion au remote
    if ! git ls-remote origin > /dev/null 2>&1; then
        log_warning "Impossible de contacter le remote 'origin'"
        log_warning "Le script continuera mais le push pourrait échouer"
    fi
    
    # Vérifier les permissions du dossier .git
    if [ ! -w ".git/objects" ]; then
        log_error "Permissions insuffisantes sur .git/objects"
        log_info "Tentative de correction des permissions..."
        if ! chmod -R 755 .git 2>/dev/null; then
            log_error "Correction automatique échouée"
            log_info "Exécutez manuellement : sudo chown -R \$(whoami):\$(whoami) .git"
            exit 1
        fi
        log_success "Permissions corrigées"
    fi
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
        if ! git switch dev; then
            log_error "Échec du changement vers dev"
            exit 1
        fi
    else
        log_info "Création de la branche dev depuis origin/dev"
        if ! git checkout -b dev origin/dev 2>/dev/null; then
            log_error "Impossible de créer la branche dev"
            log_info "Vérifiez que origin/dev existe"
            exit 1
        fi
    fi
}

# --- Fonction de mise à jour depuis le remote ---
update_from_remote() {
    log_info "Mise à jour depuis origin/dev..."
    
    if ! git fetch origin dev; then
        log_warning "Échec du fetch depuis origin/dev"
        return 1
    fi
    
    local local_commit=$(git rev-parse dev)
    local remote_commit=$(git rev-parse origin/dev)
    
    if [ "$local_commit" = "$remote_commit" ]; then
        log_success "Branche dev déjà à jour"
        return 0
    fi
    
    log_info "Tentative de mise à jour fast-forward..."
    if git merge --ff-only origin/dev; then
        log_success "Mise à jour fast-forward réussie"
    else
        log_warning "Fast-forward impossible - branches divergentes"
        log_info "Vous devrez résoudre manuellement les conflits"
        return 1
    fi
}

# --- Fonction d'analyse des fichiers modifiés ---
analyze_changes() {
    log_info "Analyse des modifications en cours..."
    
    echo -e "\n${BLUE}📊 État du working directory :${NC}"
    git status -sb
    
    local modified_count=$(git status --porcelain | grep -E '^ M' | wc -l)
    local deleted_count=$(git status --porcelain | grep -E '^ D' | wc -l)
    local untracked_count=$(git status --porcelain | grep -E '^\?\?' | wc -l)
    
    echo -e "\n${BLUE}📈 Résumé des changements :${NC}"
    echo "  Modifiés: $modified_count fichiers"
    echo "  Supprimés: $deleted_count fichiers" 
    echo "  Non suivis: $untracked_count fichiers"
    
    # Vérifier les fichiers volumineux
    echo -e "\n${BLUE}⚖️  Vérification des fichiers >100 Mo :${NC}"
    local large_files=$(find . -type f -size +100M ! -path "./.git/*" 2>/dev/null | head -10)
    if [ -n "$large_files" ]; then
        echo "$large_files" | while read file; do
            local size=$(du -h "$file" | cut -f1)
            log_warning "Fichier volumineux détecté: $file ($size)"
        done
        log_info "Ces fichiers ne seront PAS commités automatiquement"
    else
        log_success "Aucun fichier volumineux détecté"
    fi
}

# --- Fonction d'ajout sécurisé des fichiers ---
safe_add_files() {
    log_info "Ajout sécurisé des fichiers..."

    # Ne PAS ajouter automatiquement les fichiers non suivis
    # Ajoute uniquement :
    #   - fichiers MODIFIÉS
    #   - fichiers SUPPRIMÉS
    # Jamais de nouveaux fichiers (sauf si le user le fait volontairement)
    git add -u

    # Affiche ce qui sera committé
    log_info "📦 Contenu du staging area :"
    git diff --cached --name-only

    log_success "Ajout sécurisé effectué (git add -u)"
}


# --- Fonction de création du commit ---
create_commit() {
    local commit_msg="${1:-"MAJ dev $(date '+%Y-%m-%d %H:%M:%S')"}"
    
    log_info "Création du commit..."
    
    if git diff --cached --quiet; then
        log_warning "Aucune modification à committer"
        return 1
    fi
    
    if git commit -m "$commit_msg"; then
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
    
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if git push origin dev; then
            log_success "Push réussi vers origin/dev"
            return 0
        else
            retry_count=$((retry_count + 1))
            log_warning "Échec du push (tentative $retry_count/$max_retries)"
            
            if [ $retry_count -lt $max_retries ]; then
                log_info "Nouvelle tentative dans 5 secondes..."
                sleep 5
            else
                log_error "Échec du push après $max_retries tentatives"
                log_info "Vérifiez :"
                log_info "  - La connexion réseau"
                log_info "  - Les permissions sur le dépôt distant"
                log_info "  - Les éventuels conflits à résoudre"
                return 1
            fi
        fi
    done
}

# --- Fonction de nettoyage ---
cleanup() {
    log_info "Nettoyage des ressources..."
    # Ajouter ici toute opération de nettoyage si nécessaire
    log_success "Nettoyage terminé"
}

# --- Fonction principale ---
main() {
    local commit_message="${1:-"MAJ dev $(date '+%Y-%m-%d %H:%M:%S')"}"
    
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}🚀 GIT DEV - Déploiement sur la branche dev${NC}"
    echo -e "${BLUE}================================================================${NC}"
    
    # Obtenir le chemin racine du dépôt
    REPO_ROOT=$(git rev-parse --show-toplevel)
    cd "$REPO_ROOT"
    log_info "Dépôt: $REPO_ROOT"
    
    # Exécution du workflow
    check_prerequisites
    switch_to_dev
    update_from_remote
    analyze_changes
    safe_add_files
    
    if create_commit "$commit_message"; then
        safe_push
    else
        log_warning "Aucun push effectué (rien à committer)"
    fi
    
    cleanup
    
    echo -e "${GREEN}================================================================${NC}"
    echo -e "${GREEN}✨ Script terminé avec succès${NC}"
    echo -e "${GREEN}================================================================${NC}"
}

# --- Gestion des signaux ---
trap cleanup EXIT

# --- Point d'entrée du script ---
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main "$@"
fi