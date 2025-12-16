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
# 2️⃣ Activation de l'environnement virtuel Python (HOST SEULEMENT)
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 0 ]; then
    VENV_PATH="/home/datascientest/cde/cde_env"

    if [ -d "$VENV_PATH" ]; then
        echo "------------------------------------------------------------"
        echo "Activation de l'environnement Python : $VENV_PATH"
        # shellcheck disable=SC1090
        source "$VENV_PATH/bin/activate"
        echo "Python utilisé : $(which python)"
        echo "Version Python : $(python --version)"
        echo "------------------------------------------------------------"
    else
        echo "⚠️ Environnement virtuel introuvable : $VENV_PATH"
        echo "   Les imports Python risquent d'échouer (dotenv, torch, emoji...)."
    fi
fi

# -------------------------------------------------------------
# 3️⃣ Chargement du .env
# -------------------------------------------------------------
if [ -f "$ENV_FILE" ]; then
    set -a
    . "$ENV_FILE"
    set +a
else
    echo "⚠️ Fichier .env introuvable : $ENV_FILE"
fi

# -------------------------------------------------------------
# 4️⃣ Normalisation des chemins
# -------------------------------------------------------------
if [ "$IN_DOCKER" -eq 1 ]; then
    LOG_DIR="${LOG_DIR/$HOST_BASE/$DOCKER_BASE}"
fi

# Fallback
if [ -z "${LOG_DIR:-}" ]; then
    LOG_DIR="${BASE_DIR}/logs"
fi
mkdir -p "$LOG_DIR"

# -------------------------------------------------------------
# 5️⃣ Log principal
# -------------------------------------------------------------
LOG_FILE="${LOG_DIR}/run_all_ml_$(date '+%Y-%m-%d_%H-%M-%S').log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "============================================================"
echo "🟪 LANCEMENT DU PIPELINE MACHINE LEARNING"
[ "$IN_DOCKER" -eq 1 ] && echo "➡️ Mode : Docker/Airflow" || echo "➡️ Mode : Host"
echo "LOG_FILE : $LOG_FILE"
echo "============================================================"

# -------------------------------------------------------------
# 6️⃣ Liste ORDONNÉE des scripts ML
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
# 7️⃣ Fonction générique d'exécution Python
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

    # IMPORTANT : utiliser "python" pour profiter du venv activé
    if python "$script"; then
        echo "✅ Terminé : $name"
        return 0
    else
        echo "❌ Échec : $name"
        return 1
    fi
}

# -------------------------------------------------------------
# 8️⃣ Pipeline séquentiel
# -------------------------------------------------------------
overall_status=0

for script in "${SCRIPTS[@]}"; do
    run_python "$script" || overall_status=1
done

# -------------------------------------------------------------
# 9️⃣ Résultat final
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
