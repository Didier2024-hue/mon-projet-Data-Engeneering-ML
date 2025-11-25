#!/bin/bash
set -euo pipefail

# =============================================================================
# GIT MAIN - Script de déploiement pour la branche main (production)
# Version sécurisée avec validation et processus de release
# =============================================================================

# --- Configuration des couleurs ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# --- Fonctions de logging ---
log_info() { echo -e "${BLUE}ℹ️ $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }
log_warning() { echo -e "${YELLOW}⚠️ $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() { echo -e "${PURPLE}🔸 $1${NC}"; }

# --- Fonction de vérification de l'environnement ---
check_environment() {
    log_info "Vérification de l'environnement de production..."
    
    # Vérifier qu'on est dans un dépôt Git
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Ce répertoire n'est pas un dépôt Git"
        exit 1
    fi
    
    # Vérifier la branche actuelle
    local current_branch=$(git branch --show-current)
    if [ "$current_branch" != "dev" ]; then
        log_warning "Vous n'êtes pas sur la branche 'dev' (actuellement: $current_branch)"
        log_info "Le script fonctionne mieux depuis la branche dev"
    fi
    
    # Vérifier l'état du working directory
    if ! git diff --quiet; then
        log_warning "Des modifications non commitées sont présentes"
        log_info "Il est recommandé de committer ou stash vos changements avant de continuer"
    fi
}

# --- Fonction de vérification des prérequis pour main ---
check_main_prerequisites() {
    log_step "Vérification des prérequis pour le déploiement main..."
    
    # Vérifier que dev est à jour avec origin/dev
    if ! git fetch origin dev; then
        log_error "Impossible de récupérer les dernières modifications de dev"
        exit 1
    fi
    
    local local_dev=$(git rev-parse dev)
    local remote_dev=$(git rev-parse origin/dev)
    
    if [ "$local_dev" != "$remote_dev" ]; then
        log_error "La branche dev n'est pas à jour avec origin/dev"
        log_info "Exécutez d'abord: git pull origin dev"
        exit 1
    fi
    
    # Vérifier que main existe
    if ! git show-ref --verify --quiet refs/heads/main; then
        log_error "Branche main non trouvée localement"
        exit 1
    fi
    
    # Vérifier la connexion au remote
    if ! git ls-remote origin main > /dev/null 2>&1; then
        log_error "Impossible de contacter le remote 'origin' pour main"
        exit 1
    fi
    
    log_success "Prérequis validés"
}

# --- Fonction de vérification de l'état de main ---
check_main_status() {
    log_step "Analyse de l'état de la branche main..."
    
    # Récupérer les dernières informations
    git fetch origin main
    
    local main_local=$(git rev-parse main)
    local main_remote=$(git rev-parse origin/main)
    
    echo -e "${BLUE}📊 État des branches :${NC}"
    echo "  main local:  $main_local"
    echo "  main remote: $main_remote"
    echo "  dev:         $(git rev-parse dev)"
    
    if [ "$main_local" != "$main_remote" ]; then
        log_warning "La branche main locale n'est pas à jour avec origin/main"
        log_info "Mise à jour de main..."
        git checkout main
        git pull origin main
        git checkout dev
    fi
    
    # Vérifier si main est en avance sur dev (ce qui serait problématique)
    if git merge-base --is-ancestor dev main; then
        log_success "main est à jour par rapport à dev"
    else
        log_error "La branche main a des commits non présents dans dev"
        log_info "Ceci est inhabituel - vérifiez l'historique des branches"
        exit 1
    fi
}

# --- Fonction de validation du merge ---
validate_merge() {
    log_step "Validation du merge..."
    
    # Vérifier les conflits potentiels
    if ! git merge-tree `git merge-base dev main` dev main | grep -q "changed in both"; then
        log_success "Aucun conflit détecté"
    else
        log_warning "Conflits potentiels détectés"
        log_info "Préparation à la résolution manuelle des conflits"
    fi
    
    # Vérifier les fichiers volumineux
    log_info "Vérification des fichiers volumineux..."
    local large_files=$(git ls-tree -r dev --name-only | xargs -I {} find {} -size +10M 2>/dev/null | head -5)
    if [ -n "$large_files" ]; then
        log_warning "Fichiers volumineux détectés dans dev:"
        echo "$large_files" | while read file; do
            local size=$(du -h "$file" 2>/dev/null | cut -f1 || echo "inconnu")
            echo "  - $file ($size)"
        done
    fi
}

# --- Fonction de confirmation utilisateur ---
get_user_confirmation() {
    local commit_message="$1"
    
    echo -e "${YELLOW}================================================================${NC}"
    echo -e "${YELLOW}🚀 RÉSUMÉ DU DÉPLOIEMENT VERS MAIN${NC}"
    echo -e "${YELLOW}================================================================${NC}"
    echo -e "Message de commit: ${BLUE}$commit_message${NC}"
    echo -e "De: ${GREEN}dev ($(git rev-parse --short dev))${NC}"
    echo -e "Vers: ${RED}main ($(git rev-parse --short main))${NC}"
    echo -e ""
    echo -e "Modifications à merger:"
    git log --oneline main..dev
    
    echo -e ""
    echo -e "${YELLOW}⚠️  CONFIRMER LE DÉPLOIEMENT EN PRODUCTION ?${NC}"
    echo -e "Cette action va:"
    echo -e "  ✅ Merger dev dans main"
    echo -e "  ✅ Créer un tag de release"
    echo -e "  ✅ Pousser vers origin/main"
    echo -e ""
    read -p "Confirmer (o/N) ? " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[OoYy]$ ]]; then
        log_info "Déploiement annulé"
        exit 0
    fi
}

# --- Fonction de merge vers main ---
merge_to_main() {
    local commit_message="$1"
    
    log_step "Merge de dev vers main..."
    
    # Passer sur main
    if ! git checkout main; then
        log_error "Impossible de passer sur main"
        exit 1
    fi
    
    # Mettre à jour main
    if ! git pull origin main; then
        log_error "Échec de la mise à jour de main"
        git checkout dev
        exit 1
    fi
    
    # Effectuer le merge
    log_info "Merge en cours..."
    if git merge --no-ff dev -m "Merge dev -> main: $commit_message"; then
        log_success "Merge réussi"
    else
        log_error "Merge échoué - conflits à résoudre"
        log_info "Résolvez les conflits puis: git commit -m 'Merge dev -> main: $commit_message'"
        log_info "Ensuite, terminez manuellement: git push origin main"
        exit 1
    fi
}

# --- Fonction de création de tag ---
create_release_tag() {
    log_step "Création du tag de release..."
    
    local version_tag="v$(date '+%Y.%m.%d.%H%M')"
    local commit_message="Release $version_tag"
    
    if git tag -a "$version_tag" -m "$commit_message"; then
        log_success "Tag créé: $version_tag"
        echo "$version_tag"
    else
        log_warning "Échec de la création du tag"
        return 1
    fi
}

# --- Fonction de push vers main ---
push_to_main() {
    local tag_name="$1"
    
    log_step "Push vers origin/main..."
    
    if git push origin main; then
        log_success "Push de main réussi"
    else
        log_error "Échec du push vers main"
        git checkout dev
        exit 1
    fi
    
    # Pousser le tag si il existe
    if [ -n "$tag_name" ] && git show-ref --verify --quiet "refs/tags/$tag_name"; then
        if git push origin "$tag_name"; then
            log_success "Tag $tag_name poussé avec succès"
        else
            log_warning "Échec du push du tag"
        fi
    fi
}

# --- Fonction de retour à dev ---
return_to_dev() {
    log_step "Retour à la branche dev..."
    
    if git checkout dev; then
        log_success "Retour à dev réussi"
    else
        log_error "Impossible de retourner sur dev"
        exit 1
    fi
}

# --- Fonction de rapport final ---
generate_report() {
    local tag_name="$1"
    local commit_message="$2"
    
    echo -e "${GREEN}================================================================${NC}"
    echo -e "${GREEN}🎉 DÉPLOIEMENT RÉUSSI${NC}"
    echo -e "${GREEN}================================================================${NC}"
    echo -e "${BLUE}📋 Résumé :${NC}"
    echo -e "  Message: $commit_message"
    echo -e "  Tag: ${tag_name:-"Aucun"}"
    echo -e "  Commit: $(git rev-parse --short main)"
    echo -e ""
    echo -e "${BLUE}🔗 Actions disponibles :${NC}"
    echo -e "  Voir les différences: ${GREEN}git log --oneline main..dev${NC}"
    echo -e "  Voir le dernier tag: ${GREEN}git describe --tags --abbrev=0${NC}"
    echo -e "  Revenir à dev: ${GREEN}git checkout dev${NC}"
}

# --- Fonction de nettoyage ---
cleanup() {
    log_info "Nettoyage en cours..."
    # S'assurer qu'on retourne sur dev en cas d'erreur
    if [ "$(git branch --show-current)" != "dev" ]; then
        git checkout dev >/dev/null 2>&1 || true
    fi
    log_success "Nettoyage terminé"
}

# --- Fonction principale ---
main() {
    local commit_message="${1:-"Merge dev -> main $(date '+%Y-%m-%d %H:%M:%S')"}"
    
    echo -e "${PURPLE}================================================================${NC}"
    echo -e "${PURPLE}🚀 GIT MAIN - Déploiement en production${NC}"
    echo -e "${PURPLE}================================================================${NC}"
    
    # Configuration du trap pour le nettoyage
    trap cleanup EXIT
    
    # Workflow de déploiement
    check_environment
    check_main_prerequisites
    check_main_status
    validate_merge
    get_user_confirmation "$commit_message"
    
    local tag_name=""
    if merge_to_main "$commit_message"; then
        tag_name=$(create_release_tag)
        push_to_main "$tag_name"
        return_to_dev
        generate_report "$tag_name" "$commit_message"
    else
        log_error "Le déploiement a échoué"
        exit 1
    fi
}

# --- Point d'entrée du script ---
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    main "$@"
fi