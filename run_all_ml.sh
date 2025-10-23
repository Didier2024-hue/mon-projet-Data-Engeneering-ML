#!/bin/bash

LOGFILE_ML="/home/datascientest/cde/run_all_ml.log"

# Fonction pour obtenir la date et l'heure actuelles
get_timestamp() {
    date '+%Y-%m-%d %H:%M:%S'
}

# Fonction pour calculer la durée
calculate_duration() {
    local start=$1
    local end=$2
    local diff=$((end - start))
    
    local hours=$((diff / 3600))
    local minutes=$(( (diff % 3600) / 60 ))
    local seconds=$((diff % 60))
    
    printf "%02dh %02dm %02ds" $hours $minutes $seconds
}

echo "=== Début du processus global - $(get_timestamp) ===" | tee -a "$LOGFILE_ML"

# Script 1
start_time=$(date +%s)
echo "Début de snapshot_data.py - $(get_timestamp)" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/preprocess/snapshot_data.py 2>&1 | tee -a "$LOGFILE_ML"
end_time=$(date +%s)
duration=$(calculate_duration $start_time $end_time)
echo "Fin de snapshot_data.py - $(get_timestamp) - Durée: $duration" | tee -a "$LOGFILE_ML"
echo "----------------------------------------" | tee -a "$LOGFILE_ML"

# Script 2
start_time=$(date +%s)
echo "Début de sentiment_analysis.py - $(get_timestamp)" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/preprocess/sentiment_analysis.py 2>&1 | tee -a "$LOGFILE_ML"
end_time=$(date +%s)
duration=$(calculate_duration $start_time $end_time)
echo "Fin de sentiment_analysis.py - $(get_timestamp) - Durée: $duration" | tee -a "$LOGFILE_ML"
echo "----------------------------------------" | tee -a "$LOGFILE_ML"

# Script 3
start_time=$(date +%s)
echo "Début de clean_data.py - $(get_timestamp)" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/preprocess/clean_data.py 2>&1 | tee -a "$LOGFILE_ML"
end_time=$(date +%s)
duration=$(calculate_duration $start_time $end_time)
echo "Fin de clean_data.py - $(get_timestamp) - Durée: $duration" | tee -a "$LOGFILE_ML"
echo "----------------------------------------" | tee -a "$LOGFILE_ML"

# Script 4
start_time=$(date +%s)
echo "Début de preprocess_clean_avis.py - $(get_timestamp)" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/preprocess/preprocess_clean_avis.py 2>&1 | tee -a "$LOGFILE_ML"
end_time=$(date +%s)
duration=$(calculate_duration $start_time $end_time)
echo "Fin de preprocess_clean_avis.py - $(get_timestamp) - Durée: $duration" | tee -a "$LOGFILE_ML"
echo "----------------------------------------" | tee -a "$LOGFILE_ML"

# Script 5
start_time=$(date +%s)
echo "Début du modele de prédiction - $(get_timestamp)" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/models/train_dual_models.py 2>&1 | tee -a "$LOGFILE_ML"
end_time=$(date +%s)
duration=$(calculate_duration $start_time $end_time)
echo "Fin du modele de prédiction - $(get_timestamp) - Durée: $duration" | tee -a "$LOGFILE_ML"
echo "----------------------------------------" | tee -a "$LOGFILE_ML"

# Durée totale
global_start_time=$(date +%s)
echo "=== Tous les scripts sont terminés - $(get_timestamp) ===" | tee -a "$LOGFILE_ML"
total_duration=$(calculate_duration $global_start_time $(date +%s))
echo "=== DURÉE TOTALE: $total_duration ===" | tee -a "$LOGFILE_ML"
