#!/bin/bash

# ==============================================================
# Script : run_all_scraping.sh
# Objectif : Lancer le scraping Trustpilot pour plusieurs sociétés
# Auteur : Didier (projet DataScientest)
# ==============================================================
# Chaque exécution génère un log horodaté unique
# ==============================================================

# Chargement des variables d'environnement
if [ -f .env ]; then
    export $(grep -v '#' .env | awk '/=/ {print $1}')
else
    echo "⚠️  Fichier .env non trouvé. Certaines variables peuvent manquer."
fi

# Répertoire et fichier de logs horodatés
LOG_DIR="/home/datascientest/cde/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/run_all_scraping_$(date '+%Y-%m-%d_%H-%M-%S').log"

# Redirection de la sortie vers le fichier de log + console
exec > >(tee -a "$LOG_FILE") 2>&1

# ==============================================================
# Fonctions utilitaires
# ==============================================================

get_timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

calculate_duration() {
    local start=$1
    local end=$2
    local diff=$((end - start))
    local hours=$((diff / 3600))
    local minutes=$(((diff % 3600) / 60))
    local seconds=$((diff % 60))
    printf "%02dh %02dm %02ds" $hours $minutes $seconds
}

# Vérifie la connexion Internet (HTTP, pas ping)
check_internet_connection() {
    if curl -Is --max-time 5 https://www.trustpilot.com | grep -q "HTTP"; then
        return 0
    else
        echo "❌ ERREUR: Impossible d'accéder à https://www.trustpilot.com - problème réseau ou DNS"
        return 1
    fi
}

# Retourne la dernière page scrapée
get_last_page() {
    local societe=$1
    local domain_name=$(echo "$societe" | cut -d'.' -f1)
    local domain_dir="${DATA_RAW_TRUSTPILOT}/${domain_name}"
    local last_page_file="${domain_dir}/derniere_page.txt"

    if [ -f "$last_page_file" ]; then
        cat "$last_page_file" 2>/dev/null
    else
        echo "0"
    fi
}

# Scraper une société donnée
scraper_societe() {
    local societe=$1
    local last_page=$(get_last_page "$societe")
    local start_page=$((last_page + 1))

    echo "------------------------------------------------------------"
    echo "[$(get_timestamp)] Début du scraping : $societe"
    echo "Dernière page : $last_page | Prochaine : $start_page | Pages max : $MAX_PAGES"
    echo "------------------------------------------------------------"

    local start_time=$(date +%s)

    if ! check_internet_connection; then
        echo "⚠️  Connexion indisponible, pause 10 secondes..."
        sleep 10
        return 1
    fi

    # Exécution du scraping Python
    if echo -e "$societe\n$MAX_PAGES" | python3 "$SCRIPT_PYTHON"; then
        local end_time=$(date +%s)
        local duration=$(calculate_duration $start_time $end_time)
        local new_last_page=$(get_last_page "$societe")
        echo "✅ SUCCÈS: Scraping de $societe terminé — Durée : $duration"
        echo "Nouvelle dernière page : $new_last_page"
        return 0
    else
        local end_time=$(date +%s)
        local duration=$(calculate_duration $start_time $end_time)
        echo "❌ ÉCHEC: Scraping de $societe — Durée : $duration"
        return 1
    fi
}

afficher_resume() {
    echo "============================================================"
    echo "RÉSUMÉ DES DERNIÈRES PAGES SCRAPÉES — $(get_timestamp)"
    echo "Répertoire des données : $DATA_RAW_TRUSTPILOT"
    echo "============================================================"
    for societe in "${SOCIETES[@]}"; do
        local last_page=$(get_last_page "$societe")
        local domain_name=$(echo "$societe" | cut -d'.' -f1)
        echo "$societe : dernière page = $last_page"
    done
}

# ==============================================================
# Configuration et lancement
# ==============================================================

echo "============================================================" 
echo "=== LANCEMENT DU SCRAPING TRUSTPILOT ==="
echo "Date de lancement : $(get_timestamp)"
echo "Fichier de log : $LOG_FILE"
echo "============================================================"

# Vérification du script Python
SCRIPT_PYTHON="${BASE_DIR}/scripts/scraping/cde_scrap_new.py"
if [ ! -f "$SCRIPT_PYTHON" ]; then
    echo "❌ Erreur : Le script Python $SCRIPT_PYTHON n'existe pas."
    exit 1
fi

# Liste des sociétés à scraper
SOCIETES=("temu.com" "chronopost.fr" "tesla.com" "vinted.fr")

# Paramètres
MAX_PAGES=2

# Affichage de la config
echo "BASE_DIR             : $BASE_DIR"
echo "DATA_RAW_TRUSTPILOT  : $DATA_RAW_TRUSTPILOT"
echo "Script Python        : $SCRIPT_PYTHON"
echo ""

# Résumé initial
afficher_resume
echo ""

global_start_time=$(date +%s)

# Boucle principale
for societe in "${SOCIETES[@]}"; do
    if scraper_societe "$societe"; then
        sleep_time=$((10 + RANDOM % 11))
        echo "⏳ Attente de ${sleep_time}s avant le prochain scraping..."
        sleep $sleep_time
    else
        echo "⚠️  Passage à la société suivante après erreur."
        sleep 5
    fi
done

# Résumé final
global_end_time=$(date +%s)
total_duration=$(calculate_duration $global_start_time $global_end_time)

echo ""
afficher_resume
echo ""
echo "============================================================"
echo "✅ FIN DU SCRAPING TRUSTPILOT — $(get_timestamp)"
echo "Durée totale : $total_duration"
echo "Logs complets : $LOG_FILE"
echo "============================================================"
