#!/bin/bash

# === Configuration des logs ===
LOG_DIR="/home/datascientest/cde/logs"
mkdir -p "$LOG_DIR"

# Fichier de log horodaté (ex : run_all_ml_2025-10-24_14-30-12.log)
LOGFILE_ML="${LOG_DIR}/run_all_ml_$(date '+%Y-%m-%d_%H-%M-%S').log"

# Fonction pour obtenir la date et l'heure actuelles
get_timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Fonction pour calculer la durée entre deux timestamps
calculate_duration() {
    local start=$1
    local end=$2
    local diff=$((end - start))

    local hours=$((diff / 3600))
    local minutes=$(((diff % 3600) / 60))
    local seconds=$((diff % 60))

    printf "%02dh %02dm %02ds" $hours $minutes $seconds
}

# Démarrage du log
echo "========================================================" | tee -a "$LOGFILE_ML"
echo "=== DÉBUT DU PIPELINE MACHINE LEARNING ===" | tee -a "$LOGFILE_ML"
echo "Date de lancement : $(get_timestamp)" | tee -a "$LOGFILE_ML"
echo "========================================================" | tee -a "$LOGFILE_ML"

# Enregistre le temps de début global
global_start_time=$(date +%s)

# Liste ordonnée des scripts à exécuter
declare -A SCRIPTS=(
  ["snapshot_data.py"]="/home/datascientest/cde/scripts/preprocess/snapshot_data.py"
  ["sentiment_analysis.py"]="/home/datascientest/cde/scripts/preprocess/sentiment_analysis.py"
  ["clean_data.py"]="/home/datascientest/cde/scripts/preprocess/clean_data.py"
  ["preprocess_clean_avis.py"]="/home/datascientest/cde/scripts/preprocess/preprocess_clean_avis.py"
  ["train_dual_models.py"]="/home/datascientest/cde/scripts/models/train_dual_models.py"
)

# Boucle sur chaque script
for script_name in "${!SCRIPTS[@]}"; do
    echo "--------------------------------------------------------" | tee -a "$LOGFILE_ML"
    echo "[$(get_timestamp)] DÉBUT DU SCRIPT : $script_name" | tee -a "$LOGFILE_ML"
    echo "--------------------------------------------------------" | tee -a "$LOGFILE_ML"

    start_time=$(date +%s)
    python3 "${SCRIPTS[$script_name]}" 2>&1 | tee -a "$LOGFILE_ML"
    end_time=$(date +%s)

    duration=$(calculate_duration $start_time $end_time)
    echo "--------------------------------------------------------" | tee -a "$LOGFILE_ML"
    echo "[$(get_timestamp)] FIN DU SCRIPT : $script_name — Durée : $duration" | tee -a "$LOGFILE_ML"
    echo "" | tee -a "$LOGFILE_ML"
done

# Calcul du temps total
global_end_time=$(date +%s)
total_duration=$(calculate_duration $global_start_time $global_end_time)

echo "========================================================" | tee -a "$LOGFILE_ML"
echo "=== TOUS LES SCRIPTS SONT TERMINÉS ===" | tee -a "$LOGFILE_ML"
echo "Heure de fin : $(get_timestamp)" | tee -a "$LOGFILE_ML"
echo "Durée totale : $total_duration" | tee -a "$LOGFILE_ML"
echo "========================================================" | tee -a "$LOGFILE_ML"

# Fin
exit 0
