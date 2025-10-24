#!/bin/bash

# ==============================================================
# Script : run_all.sh
# Objectif : Orchestration globale du pipeline Data Scientest
# Étapes : 1) Scraping  2) Insertion  3) Machine Learning
# Auteur : Didier
# ==============================================================

BASE_DIR="/home/datascientest/cde"
LOG_DIR="${BASE_DIR}/logs"
mkdir -p "$LOG_DIR"

# Fichier de log horodaté (ex : run_all_2025-10-24_15-25-12.log)
LOGFILE_MAIN="${LOG_DIR}/run_all_$(date '+%Y-%m-%d_%H-%M-%S').log"

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

log_message() {
    echo "[$(get_timestamp)] $1" | tee -a "$LOGFILE_MAIN"
}

# Fonction pour exécuter un script avec log et durée
run_script() {
    local phase_name="$1"
    local script_path="$2"
    local phase_log="${LOG_DIR}/$(basename "$script_path" .sh)_$(date '+%Y-%m-%d_%H-%M-%S').log"

    log_message "------------------------------------------------------------"
    log_message "PHASE : $phase_name"
    log_message "Script : $script_path"
    log_message "Log : $phase_log"
    log_message "------------------------------------------------------------"

    if [ ! -f "$script_path" ]; then
        log_message "❌ ERREUR : Script introuvable à $script_path"
        return 1
    fi

    local start_time=$(date +%s)
    bash "$script_path" > >(tee -a "$phase_log") 2>&1
    local result=$?
    local end_time=$(date +%s)
    local duration=$(calculate_duration $start_time $end_time)

    if [ $result -eq 0 ]; then
        log_message "✅ SUCCÈS : $phase_name terminée avec succès (Durée : $duration)"
    else
        log_message "❌ ÉCHEC : $phase_name — Durée : $duration"
    fi
    echo "" | tee -a "$LOGFILE_MAIN"

    return $result
}

# ==============================================================
# Lancement global
# ==============================================================

log_message "============================================================"
log_message "🚀 DÉBUT DE L'ORCHESTRATION GLOBALE"
log_message "Dossier de logs : $LOG_DIR"
log_message "============================================================"

global_start_time=$(date +%s)
global_status=0

# Phase 1 : Scraping
run_script "PHASE 1 — SCRAPING DES DONNÉES" "${BASE_DIR}/run_all_scraping.sh"
phase1_status=$?

# Pause courte
sleep 5

# Phase 2 : Insertion
run_script "PHASE 2 — INSERTION DANS LA BASE" "${BASE_DIR}/run_all_insert.sh"
phase2_status=$?

# Pause courte
sleep 5

# Phase 3 : Machine Learning
run_script "PHASE 3 — TRAITEMENT MACHINE LEARNING" "${BASE_DIR}/run_all_ml.sh"
phase3_status=$?

# ==============================================================
# Résumé final
# ==============================================================

global_end_time=$(date +%s)
total_duration=$(calculate_duration $global_start_time $global_end_time)

echo "" | tee -a "$LOGFILE_MAIN"
log_message "============================================================"
log_message "🧾 RÉSUMÉ FINAL D'EXÉCUTION"
log_message "============================================================"

[[ $phase1_status -eq 0 ]] && log_message "✅ PHASE 1 : Scraping OK" || { log_message "❌ PHASE 1 : Scraping ÉCHEC"; global_status=1; }
[[ $phase2_status -eq 0 ]] && log_message "✅ PHASE 2 : Insertion OK" || { log_message "❌ PHASE 2 : Insertion ÉCHEC"; global_status=1; }
[[ $phase3_status -eq 0 ]] && log_message "✅ PHASE 3 : Machine Learning OK" || { log_message "❌ PHASE 3 : Machine Learning ÉCHEC"; global_status=1; }

log_message "------------------------------------------------------------"
log_message "Durée totale d'exécution : $total_duration"
log_message "Log principal : $LOGFILE_MAIN"
log_message "Détails logs :"
log_message "  - Scraping   : ${LOG_DIR}/run_all_scraping_*.log"
log_message "  - Insertion  : ${LOG_DIR}/run_all_insert_*.log"
log_message "  - ML         : ${LOG_DIR}/run_all_ml_*.log"
log_message "============================================================"

if [ $global_status -eq 0 ]; then
    log_message "✅ ORCHESTRATION COMPLÈTE — TOUS LES SCRIPTS ONT RÉUSSI 🎉"
else
    log_message "⚠️ ORCHESTRATION TERMINÉE AVEC DES ERREURS"
fi

exit $global_status
