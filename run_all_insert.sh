#!/bin/bash

# =============================================================
# Script : run_all_insert.sh
# Objectif : Insertion Wiki + PostgreSQL + MongoDB
# Compatible Host + Docker/Airflow
# =============================================================

# -------------------------------------------------------------
# 1) Détection environnement
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

# 🔥 Activation du venv correct si on est sur le HOST
if [ "$IN_DOCKER" -eq 0 ]; then
    if [ -f "/home/datascientest/cde/cde_env/bin/activate" ]; then
        echo "🔧 Activation de l'environnement virtuel..."
        source /home/datascientest/cde/cde_env/bin/activate
    else
        echo "⚠️ Attention : venv introuvable : /home/datascientest/cde/cde_env"
    fi
fi

ENV_FILE="${BASE_DIR}/.env"

# -------------------------------------------------------------
# 2) Chargement .env
# -------------------------------------------------------------
if [ -f "$ENV_FILE" ]; then
    set -a
    . "$ENV_FILE"
    set +a
else
    echo "⚠️ .env introuvable : $ENV_FILE"
fi

# -------------------------------------------------------------
# 3) Normalisation des chemins
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    LOG_DIR="${LOG_DIR/$HOST_BASE/$DOCKER_BASE}"
fi

# fallback logs
if [ -z "${LOG_DIR:-}" ]; then
    LOG_DIR="${BASE_DIR}/log"
fi

mkdir -p "$LOG_DIR"
LOGFILE_INSERT="${LOG_DIR}/run_all_insert_$(date '+%Y-%m-%d_%H-%M-%S').log"

exec > >(tee -a "$LOGFILE_INSERT") 2>&1

echo "============================================================"
echo "🏁 Script run_all_insert.sh"
echo "Mode : $([ "$IN_DOCKER" -eq 1 ] && echo 'Docker' || echo 'Host')"
echo "BASE_DIR : $BASE_DIR"
echo "Log : $LOGFILE_INSERT"
echo "============================================================"

# -------------------------------------------------------------
# 4) Scripts réels (vérifiés)
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    SCRIPT_WIKI="$DOCKER_BASE/scripts/insert/cde_insert_wiki.py"
    SCRIPT_POSTGRE="$DOCKER_BASE/scripts/insert/insert_postgre.py"
    SCRIPT_MONGO="$DOCKER_BASE/scripts/insert/insert_mongodb.py"
else
    SCRIPT_WIKI="$HOST_BASE/scripts/insert/cde_insert_wiki.py"
    SCRIPT_POSTGRE="$HOST_BASE/scripts/insert/insert_postgre.py"
    SCRIPT_MONGO="$HOST_BASE/scripts/insert/insert_mongodb.py"
fi

echo "Scripts détectés :"
echo "- $SCRIPT_WIKI"
echo "- $SCRIPT_POSTGRE"
echo "- $SCRIPT_MONGO"
echo ""

# -------------------------------------------------------------
# 5) Fonction d'exécution Python
# -------------------------------------------------------------
run_python_script() {
    local script="$1"
    local label="$2"

    echo ""
    echo "------------------------------------------------------------"
    echo "🔵 Lancement : $label"
    echo "Script : $script"
    echo "------------------------------------------------------------"

    if [ ! -f "$script" ]; then
        echo "❌ Erreur : script introuvable → $script"
        return 1
    fi

    if python3 "$script"; then
        echo "✅ Succès : $label"
        return 0
    else
        echo "❌ Échec : $label"
        return 1
    fi
}

# -------------------------------------------------------------
# 6) Pipeline séquentiel
# -------------------------------------------------------------
status=0

run_python_script "$SCRIPT_WIKI"    "Insertion Wikipedia" || status=1
run_python_script "$SCRIPT_POSTGRE" "Insertion PostgreSQL" || status=1
run_python_script "$SCRIPT_MONGO"   "Insertion MongoDB" || status=1

echo ""
echo "============================================================"
if [ "$status" -eq 0 ]; then
    echo "🎉 FIN : toutes les insertions ont réussi."
else
    echo "⚠️ FIN : des erreurs ont eu lieu."
fi
echo "Log complet : $LOGFILE_INSERT"
echo "============================================================"

exit "$status"
