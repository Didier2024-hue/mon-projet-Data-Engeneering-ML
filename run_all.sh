#!/bin/bash
set -e

# ============================================================== 
# 🚀 Script : run_all.sh (exécute : Scraping → Insert → ML)
# ============================================================== 

BASE_DIR="/home/datascientest/cde"
LOG_DIR="${BASE_DIR}/logs"
mkdir -p "$LOG_DIR"

MAIN_LOG="${LOG_DIR}/run_all_$(date '+%Y-%m-%d_%H-%M-%S').log"

# 🔒 Lock unique pour empêcher toute exécution multiple
LOCK_FILE="${BASE_DIR}/.pipeline_running"

if [ -f "$LOCK_FILE" ]; then
    echo "[LOCK] ⛔ Un pipeline est déjà en cours." | tee -a "$MAIN_LOG"
    exit 1
fi

# Création du lock
echo $$ > "$LOCK_FILE"

# Suppression auto du lock, même en cas de crash
cleanup() {
    rm -f "$LOCK_FILE"
}
trap cleanup EXIT

# ============================================================== 
# UTILITAIRES
# ============================================================== 

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

duration() {
    local start=$1
    local end=$2
    local d=$((end-start))
    printf "%02dh %02dm %02ds" $((d/3600)) $(((d%3600)/60)) $((d%60))
}

log() { echo "[$(timestamp)] $1" | tee -a "$MAIN_LOG"; }

run_phase() {
    local title="$1"
    local script_path="$2"
    local phase_log="${LOG_DIR}/$(basename $script_path)_$(date '+%Y-%m-%d_%H-%M-%S').log"

    log "------------------------------------------------------------"
    log "⏳ $title"
    log "Script : $script_path"
    log "Log    : $phase_log"
    log "------------------------------------------------------------"

    if [ ! -f "$script_path" ]; then
        log "❌ ERREUR : Script introuvable ($script_path)"
        return 1
    fi

    local start=$(date +%s)

    bash "$script_path" > >(tee -a "$phase_log") 2>&1
    local status=$?

    local end=$(date +%s)
    local dur=$(duration $start $end)

    if [ $status -eq 0 ]; then
        log "✅ SUCCÈS : $title (Durée : $dur)"
    else
        log "❌ ÉCHEC : $title (Durée : $dur)"
    fi

    return $status
}

# ============================================================== 
# 🚀 EXÉCUTION DU PIPELINE
# ============================================================== 

log "============================================================"
log "🚀 DÉBUT DU PIPELINE GLOBAL CDE"
log "============================================================"

GLOBAL_START=$(date +%s)
GLOBAL_STATUS=0

run_phase "PHASE 1 — Scraping" "${BASE_DIR}/run_all_scraping.sh" || GLOBAL_STATUS=1
sleep 1

run_phase "PHASE 2 — Insertion" "${BASE_DIR}/run_all_insert.sh" || GLOBAL_STATUS=1
sleep 1

run_phase "PHASE 3 — Machine Learning" "${BASE_DIR}/run_all_ml.sh" || GLOBAL_STATUS=1

GLOBAL_END=$(date +%s)
TOTAL_DUR=$(duration $GLOBAL_START $GLOBAL_END)

log ""
log "============================================================"
log "🧾 RÉSUMÉ FINAL"
log "============================================================"

if [ $GLOBAL_STATUS -eq 0 ]; then
    log "🎉 PIPELINE GLOBAL : SUCCÈS COMPLET"
else
    log "⚠️ PIPELINE GLOBAL : TERMINÉ AVEC ERREURS"
fi

log "⏱ Durée totale : $TOTAL_DUR"
log "📄 Log principal : $MAIN_LOG"
log "============================================================"

exit $GLOBAL_STATUS
