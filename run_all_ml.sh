#!/bin/bash

# =============================================================
# Script : run_all_ml.sh
# Objectif : Exécuter séquentiellement tous les scripts ML
# Compatible HOST / Docker Airflow
# =============================================================

# -------------------------------------------------------------
# 1️⃣ Détection de l'environnement
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
    echo "⚠️ Fichier .env introuvable : $ENV_FILE"
fi

# -------------------------------------------------------------
# 3️⃣ Normalisation des chemins
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    LOG_DIR="${LOG_DIR/$HOST_BASE/$DOCKER_BASE}"
fi

# fallback LOG_DIR
if [ -z "${LOG_DIR:-}" ]; then
    LOG_DIR="${BASE_DIR}/logs"
fi
mkdir -p "$LOG_DIR"

# -------------------------------------------------------------
# 4️⃣ Log principal
# -------------------------------------------------------------
LOG_FILE="${LOG_DIR}/run_all_ml_$(date '+%Y-%m-%d_%H-%M-%S').log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "============================================================"
echo "🟪 LANCEMENT DU PIPELINE MACHINE LEARNING"
[ "$IN_DOCKER" -eq 1 ] && echo "➡️ Mode : Docker/Airflow" || echo "➡️ Mode : Host"
echo "LOG_FILE : $LOG_FILE"
echo "============================================================"

# -------------------------------------------------------------
# 5️⃣ Liste ORDONNÉE des scripts ML
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    SCRIPTS=(
      "/opt/airflow/cde/scripts/preprocess/snapshot_data.py"
      "/opt/airflow/cde/scripts/preprocess/clean_data.py"
      "/opt/airflow/cde/scripts/preprocess/preprocess_clean_avis.py"
      "/opt/airflow/cde/scripts/preprocess/sentiment_analysis.py"
      "/opt/airflow/cde/scripts/models/train_dual_models.py"
    )
else
    SCRIPTS=(
      "/home/datascientest/cde/scripts/preprocess/snapshot_data.py"
      "/home/datascientest/cde/scripts/preprocess/clean_data.py"
      "/home/datascientest/cde/scripts/preprocess/preprocess_clean_avis.py"
      "/home/datascientest/cde/scripts/preprocess/sentiment_analysis.py"
      "/home/datascientest/cde/scripts/models/train_dual_models.py"
    )
fi

# -------------------------------------------------------------
# 6️⃣ Fonction générique d'exécution Python
# -------------------------------------------------------------
run_python() {
    local script="$1"
    local name
    name=$(basename "$script")

    echo ""
    echo "------------------------------------------------------------"
    echo "▶️ Exécution du script : $name"
    echo "------------------------------------------------------------"

    if [ ! -f "$script" ]; then
        echo "❌ ERREUR : Script introuvable → $script"
        return 1
    fi

    if python3 "$script"; then
        echo "✅ Terminé : $name"
        return 0
    else
        echo "❌ Échec : $name"
        return 1
    fi
}

# -------------------------------------------------------------
# 7️⃣ Pipeline séquentiel
# -------------------------------------------------------------
overall_status=0

for script in "${SCRIPTS[@]}"; do
    run_python "$script" || overall_status=1
done

# -------------------------------------------------------------
# 8️⃣ Sortie propre
# -------------------------------------------------------------
echo ""
echo "============================================================"
if [ "$overall_status" -eq 0 ]; then
    echo "🎉 PIPELINE ML TERMINÉ AVEC SUCCÈS"
else
    echo "⚠️ Pipeline ML terminé avec erreurs"
fi
echo "📄 Log complet : $LOG_FILE"
echo "============================================================"

exit "$overall_status"
