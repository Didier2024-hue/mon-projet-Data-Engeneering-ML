#!/bin/bash

# Script pour lancer le scraping Trustpilot pour plusieurs sociétés
# Utilise les variables d'environnement du fichier .env
source .env

# Chargement des variables d'environnement
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
else
    echo "Warning: Fichier .env non trouvé."
fi

# Journalisation avec le répertoire de logs défini dans .env
LOG_FILE="/home/datascientest/cde/run_all_scraping.log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "Lancement du scraping Trustpilot"
echo "Journalisation dans: $LOG_FILE"

# Liste des sociétés à scraper
SOCIETES=("temu.com" "chronopost.fr" "tesla.com" "vinted.fr")

# Chemin vers le script Python (utilise BASE_DIR)
SCRIPT_PYTHON="${BASE_DIR}/scripts/scraping/cde_scrap_new.py"

# Répertoire de données 
DATA_DIR=${DATA_RAW_TRUSTPILOT}

# Nombre maximum de pages à scraper par société
MAX_PAGES=2

# Vérification que le script Python existe
if [ ! -f "$SCRIPT_PYTHON" ]; then
    echo "Erreur: Le script Python $SCRIPT_PYTHON n'a pas été trouvé."
    exit 1
fi

# Fonction pour vérifier la dernière page scrapée
get_last_page() {
    local societe=$1
    local domain_name=$(echo "$societe" | cut -d'.' -f1)  # Extraction du nom de domaine sans extension
    local domain_dir="$DATA_DIR/$domain_name"
    local last_page_file="$domain_dir/derniere_page.txt"
    
    if [ -f "$last_page_file" ]; then
        local last_page=$(cat "$last_page_file" 2>/dev/null)
        echo "$last_page"
    else
        echo "0"
    fi
}

# Fonction pour vérifier la connexion Internet
check_internet_connection() {
    if ping -c 1 -W 2 "trustpilot.com" >/dev/null 2>&1; then
        return 0  # Connexion OK
    else
        echo "ERREUR: Impossible de résoudre trustpilot.com - problème de connexion DNS"
        return 1  # Échec de connexion
    fi
}

# Fonction pour scraper une société
scraper_societe() {
    local societe=$1
    local last_page=$(get_last_page "$societe")
    local start_page=$((last_page + 1))
    
    echo "=============================================="
    echo "Scraping de $societe"
    echo "Dernière page scrapée: $last_page"
    echo "Prochaine page à scraper: $start_page"
    echo "Pages à scraper: $MAX_PAGES"
    echo "Répertoire de données: $DATA_DIR"
    echo "=============================================="
    echo "Début: $(date)"
    
    # Vérification de la connexion Internet avant de scraper
    if ! check_internet_connection; then
        echo "ERREUR: Problème de connexion détecté, passage à la suivante après pause"
        sleep 10  # Pause plus longue en cas de problème réseau
        return 1
    fi
    
    # Lancement du script Python
    if echo -e "$societe\n$MAX_PAGES" | python3 "$SCRIPT_PYTHON"; then
        local new_last_page=$(get_last_page "$societe")
        echo "SUCCÈS: Scraping de $societe terminé avec succès"
        echo "Nouvelle dernière page: $new_last_page"
        return 0
    else
        echo "ERREUR: Échec du scraping pour $societe, passage à la suivante"
        return 1
    fi
}

# Fonction pour afficher le résumé des dernières pages
afficher_resume() {
    echo "=============================================="
    echo "RÉSUMÉ DES DERNIÈRES PAGES SCRAPÉES"
    echo "Répertoire de données: $DATA_DIR"
    echo "=============================================="
    
    for societe in "${SOCIETES[@]}"; do
        local last_page=$(get_last_page "$societe")
        local domain_name=$(echo "$societe" | cut -d'.' -f1)
        local domain_dir="$DATA_DIR/$domain_name"
        echo "$societe : page $last_page (dossier: $domain_dir)"
    done
}

# Affichage de la configuration
echo "Configuration:"
echo "BASE_DIR: ${BASE_DIR}"
echo "DATA_RAW_TRUSTPILOT: ${DATA_RAW_TRUSTPILOT}"
echo "LOG_DIR: ${LOG_DIR}"
echo "Script Python: ${SCRIPT_PYTHON}"
echo ""

# Affichage du résumé initial
echo "Résumé initial des dernières pages scrapées:"
afficher_resume
echo ""

# Boucle sur toutes les sociétés
for societe in "${SOCIETES[@]}"; do
    if scraper_societe "$societe"; then
        # Attente aléatoire entre 10 et 20 secondes avant le prochain scraping
        sleep_time=$((10 + RANDOM % 11))
        echo "Attente de ${sleep_time} secondes avant le prochain scraping..."
        sleep $sleep_time
    else
        echo "Poursuite du script après échec pour $societe"
        # Attente plus courte en cas d'erreur
        sleep 5
    fi
done

# Affichage du résumé final
echo ""
echo "Résumé final des dernières pages scrapées:"
afficher_resume

echo ""
echo "Scraping terminé pour toutes les sociétés!"
echo "Fin: $(date)"