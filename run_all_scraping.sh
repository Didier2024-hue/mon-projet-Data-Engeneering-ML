#!/bin/bash

# =============================================================
# Script : run_all_scraping.sh (Version A - Clean & Stable)
# Objectif : Lancer le scraping Trustpilot + Wikipédia
# Compatible Host + Airflow (Docker)
# Auteur : Didier / Version refactorisée
# =============================================================


# -------------------------------------------------------------
# 1. Détection environnement (HOST vs DOCKER)
# -------------------------------------------------------------
HOST_BASE="/home/datascientest/cde"
DOCKER_BASE="/opt/airflow/cde"

if [ -f "/.dockerenv" ]; then
    IN_DOCKER=1
    BASE_DIR="$DOCKER_BASE"
else
    IN_DOCKER=0
    BASE_DIR="$HOST_BASE"
fi

ENV_FILE="${BASE_DIR}/.env"


# -------------------------------------------------------------
# 2. Chargement du .env simple et fiable
# -------------------------------------------------------------
if [ -f "$ENV_FILE" ]; then
    set -a
    . "$ENV_FILE"
    set +a
else
    echo "⚠️  WARNING : Fichier .env introuvable : $ENV_FILE"
fi


# -------------------------------------------------------------
# 3. Normalisation des chemins
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    # Remapping simple host → docker
    for var in DATA_RAW_TRUSTPILOT DATA_EXPORTS DATA_REPORT DATA_PROCESSED DATA_MODEL \
               WIKI_DATA_DIR SPACY_MODELS NLTK_DATA LOG_DIR DOCKER_DATA TMP_DIR \
               MLFLOW_ARTIFACT_ROOT API_EXPORT_DIR
    do
        eval value="\${$var}"
        if [[ -n "$value" ]]; then
            eval $var="${value/$HOST_BASE/$DOCKER_BASE}"
        fi
    done
fi

# LOG_DIR fallback
if [[ -z "${LOG_DIR:-}" ]]; then
    LOG_DIR="${BASE_DIR}/logs"
fi
mkdir -p "$LOG_DIR"


# -------------------------------------------------------------
# 4. Logfile unique & propre
# -------------------------------------------------------------
LOG_FILE="${LOG_DIR}/run_all_scraping_$(date '+%Y-%m-%d_%H-%M-%S').log"

# Toute sortie console → logfile + console
exec > >(tee -a "$LOG_FILE") 2>&1


# =============================================================
# Utilities
# =============================================================
timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

duration_hms() {
    local s=$1
    printf "%02dh %02dm %02ds" $((s/3600)) $(((s%3600)/60)) $((s%60))
}

internet_ok() {
    curl -Is --max-time 5 https://www.trustpilot.com | grep -q "HTTP"
}


# =============================================================
# Scraping Trustpilot
# =============================================================
SCRIPT_PYTHON="${BASE_DIR}/scripts/scraping/cde_scrap_new.py"

if [[ ! -f "$SCRIPT_PYTHON" ]]; then
    echo "❌ ERREUR : Script Python introuvable : $SCRIPT_PYTHON"
    exit 1
fi

SOCIETES=("temu.com" "chronopost.fr" "tesla.com" "vinted.fr")
MAX_PAGES=2


get_last_page() {
    local soc=$1
    local domain="${soc%%.*}"
    local file="${DATA_RAW_TRUSTPILOT}/${domain}/derniere_page.txt"
    [[ -f "$file" ]] && cat "$file" || echo 0
}


scraper_societe() {
    local soc=$1
    local last_page
    last_page=$(get_last_page "$soc")
    local next_page=$((last_page + 1))

    echo "------------------------------------------------------------"
    echo "[$(timestamp)] Scraping : $soc | Dernière page : $last_page"
    echo "------------------------------------------------------------"

    if ! internet_ok; then
        echo "❌ Pas d’internet — pause 10s"
        sleep 10
        return 1
    fi

    local start=$(date +%s)

    if echo -e "$soc\n$MAX_PAGES" | python3 "$SCRIPT_PYTHON"; then
        local end=$(date +%s)
        echo "✅ OK : $(duration_hms $((end-start)))"
        return 0
    else
        local end=$(date +%s)
        echo "❌ ECHEC : $(duration_hms $((end-start)))"
        return 1
    fi
}


resume_pages() {
    echo "============= RÉSUMÉ DES PAGES SCRAPÉES ============="
    echo "Répertoire RAW : $DATA_RAW_TRUSTPILOT"
    for s in "${SOCIETES[@]}"; do
        echo "$s : dernière page = $(get_last_page "$s")"
    done
    echo "======================================================"
}


# =============================================================
#  Lancement
# =============================================================
echo "============================================================"
echo "  SCRAPING TRUSTPILOT - début : $(timestamp)"
echo "  BASE_DIR : $BASE_DIR"
echo "  LOG_FILE : $LOG_FILE"
echo "============================================================"

resume_pages
echo ""

GLOBAL_START=$(date +%s)

for s in "${SOCIETES[@]}"; do
    if scraper_societe "$s"; then
        sleep $((10 + RANDOM % 10))
    else
        echo "⚠️  Passage à la société suivante..."
        sleep 5
    fi
done

GLOBAL_END=$(date +%s)
echo ""
resume_pages
echo ""

echo "============================================================"
echo " FIN SCRAPING TRUSTPILOT — $(timestamp)"
echo " Durée totale : $(duration_hms $((GLOBAL_END-GLOBAL_START)))"
echo " Log complet : $LOG_FILE"
echo "============================================================"


# =============================================================
#  Scraping Wikipedia
# =============================================================
echo ""
echo "============================================================"
echo "  SCRAPING WIKIPEDIA"
echo "============================================================"

WIKI_SCRIPT="${BASE_DIR}/scripts/scraping/cde_scrap_wiki.py"

if [[ -f "$WIKI_SCRIPT" ]]; then
    python3 "$WIKI_SCRIPT" && \
        echo "✅ Scraping Wikipedia : OK" || \
        echo "❌ Scraping Wikipedia : ECHEC"
else
    echo "❌ Script Wikipedia introuvable : $WIKI_SCRIPT"
fi

echo "============================================================"
echo "  FIN TOTALE — $(timestamp)"
echo "============================================================"
