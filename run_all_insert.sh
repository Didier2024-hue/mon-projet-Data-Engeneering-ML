#!/bin/bash

# =============================================================
# Script : run_all_insert.sh
# Objectif : Lancer tous les scripts d'insertion (Wiki / PostgreSQL / MongoDB)
# Compatible machine locale + Docker/Airflow
# =============================================================

# -------------------------------------------------------------
# 1️⃣ Détection de l'environnement (HOST vs DOCKER)
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
# 2️⃣ Chargement du .env
# -------------------------------------------------------------
if [ -f "$ENV_FILE" ]; then
    set -a
    . "$ENV_FILE"
    set +a
else
    echo "⚠️  Fichier .env introuvable : $ENV_FILE"
fi

# -------------------------------------------------------------
# 3️⃣ Normalisation des chemins issus du .env pour Docker
#     (même logique que ton script de scraping)
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    DATA_RAW_TRUSTPILOT="${DATA_RAW_TRUSTPILOT/$HOST_BASE/$DOCKER_BASE}"
    DATA_EXPORTS="${DATA_EXPORTS/$HOST_BASE/$DOCKER_BASE}"
    DATA_REPORT="${DATA_REPORT/$HOST_BASE/$DOCKER_BASE}"
    DATA_PROCESSED="${DATA_PROCESSED/$HOST_BASE/$DOCKER_BASE}"
    DATA_MODEL="${DATA_MODEL/$HOST_BASE/$DOCKER_BASE}"
    WIKI_DATA_DIR="${WIKI_DATA_DIR/$HOST_BASE/$DOCKER_BASE}"
    SPACY_MODELS="${SPACY_MODELS/$HOST_BASE/$DOCKER_BASE}"
    NLTK_DATA="${NLTK_DATA/$HOST_BASE/$DOCKER_BASE}"
    LOG_DIR="${LOG_DIR/$HOST_BASE/$DOCKER_BASE}"
    DOCKER_DATA="${DOCKER_DATA/$HOST_BASE/$DOCKER_BASE}"
    TMP_DIR="${TMP_DIR/$HOST_BASE/$DOCKER_BASE}"
    MLFLOW_ARTIFACT_ROOT="${MLFLOW_ARTIFACT_ROOT/$HOST_BASE/$DOCKER_BASE}"
    API_EXPORT_DIR="${API_EXPORT_DIR/$HOST_BASE/$DOCKER_BASE}"

    BASE_DIR="$DOCKER_BASE"
else
    BASE_DIR="$HOST_BASE"
fi

# Si LOG_DIR n'est pas défini ou vide → fallback sur BASE_DIR/logs
if [ -z "${LOG_DIR:-}" ]; then
    LOG_DIR="${BASE_DIR}/logs"
fi

# -------------------------------------------------------------
# Adaptation de la connexion PostgreSQL en environnement Docker
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    # Dans Docker, la base est accessible via le service docker-compose
    # (comme dans AIRFLOW__DATABASE__SQL_ALCHEMY_CONN)
    export POSTGRES_HOST="postgres-cde"
fi

# -------------------------------------------------------------
# Adaptation connexion MongoDB en environnement Docker
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    # 👉 À adapter : mets ici le nom/host réel de ta Mongo vue depuis Docker
    # Si tu as une Mongo dans docker-compose, par ex. service "mongo-cde":
    export MONGO_HOST="${MONGO_HOST_DOCKER:-mongo-cde}"

    # On régénère aussi MONGO_URI en cohérence
    if [ -n "${MONGO_USER:-}" ] && [ -n "${MONGO_PASSWORD:-}" ]; then
        export MONGO_URI="mongodb://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_HOST}:${MONGO_PORT:-27017}/${MONGO_DB:-trustpilot}?authSource=${MONGO_AUTH_SOURCE:-admin}"
    else
        export MONGO_URI="mongodb://${MONGO_HOST}:${MONGO_PORT:-27017}/${MONGO_DB:-trustpilot}"
    fi
fi



# -------------------------------------------------------------
# 3bis️⃣ Adaptation des variables de connexion DB en environnement Docker
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    # Dans Docker, la base est accessible via le service docker-compose
    # On ne touche PAS au .env sur le host, on override seulement ici
    export POSTGRES_HOST="postgres-cde"
fi


mkdir -p "$LOG_DIR"

LOGFILE_INSERT="${LOG_DIR}/run_all_insert_$(date '+%Y-%m-%d_%H-%M-%S').log"

# -------------------------------------------------------------
# 4️⃣ Redirection globale des logs (console + fichier)
# -------------------------------------------------------------
exec > >(tee -a "$LOGFILE_INSERT") 2>&1

echo "============================================================"
echo "🏁 LANCEMENT : run_all_insert.sh"
if [ "$IN_DOCKER" -eq 1 ]; then
    echo "Environnement : AIRFLOW / Docker"
else
    echo "Environnement : HOST (machine locale)"
fi
echo "BASE_DIR      : $BASE_DIR"
echo "LOG_DIR       : $LOG_DIR"
echo "Log fichier   : $LOGFILE_INSERT"
echo "============================================================"

# -------------------------------------------------------------
# 5️⃣ Chemins des scripts Python
# -------------------------------------------------------------
SCRIPT_WIKI="${BASE_DIR}/scripts/insert/cde_insert_wiki.py"
SCRIPT_POSTGRE="${BASE_DIR}/scripts/insert/insert_postgre.py"
SCRIPT_MONGO="${BASE_DIR}/scripts/insert/insert_mongodb.py"

# -------------------------------------------------------------
# 6️⃣ Fonction utilitaire pour exécuter un script Python
# -------------------------------------------------------------
run_python_script() {
    local script_path="$1"
    local script_name="$2"

    echo ""
    echo "------------------------------------------------------------"
    echo "🚀 Lancement : $script_name"
    echo "Script : $script_path"
    echo "------------------------------------------------------------"

    if [ ! -f "$script_path" ]; then
        echo "❌ ERREUR : Script introuvable : $script_path"
        return 1
    fi

    python3 "$script_path"
    local status=$?

    if [ "$status" -eq 0 ]; then
        echo "✅ Succès : $script_name"
        return 0
    else
        echo "❌ ERREUR lors de l'exécution de : $script_name (code=$status)"
        return "$status"
    fi
}

# -------------------------------------------------------------
# 7️⃣ Exécution séquentielle + code retour global pour Airflow
# -------------------------------------------------------------
overall_status=0

run_python_script "$SCRIPT_WIKI"    "cde_insert_wiki.py"   || overall_status=1
run_python_script "$SCRIPT_POSTGRE" "insert_postgre.py"    || overall_status=1
run_python_script "$SCRIPT_MONGO"   "insert_mongodb.py"    || overall_status=1

echo ""
echo "============================================================"
if [ "$overall_status" -eq 0 ]; then
    echo "🎉 FIN DU SCRIPT run_all_insert.sh — tous les inserts ont réussi."
else
    echo "⚠️  FIN DU SCRIPT run_all_insert.sh — une ou plusieurs erreurs sont survenues."
fi
echo "Log complet : $LOGFILE_INSERT"
echo "============================================================"

exit "$overall_status"
