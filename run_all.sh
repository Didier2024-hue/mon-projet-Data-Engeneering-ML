#!/bin/bash

# Configuration
BASE_DIR="/home/datascientest/cde"
LOGFILE_MAIN="${BASE_DIR}/run_all_scripts.log"

# Fonction pour logger les messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOGFILE_MAIN"
}

# Fonction pour exécuter un script avec gestion d'erreur
run_script() {
    local script_name="$1"
    local script_path="$2"
    
    log_message "Début de l'exécution: $script_name"
    
    if [ -f "$script_path" ]; then
        if bash "$script_path"; then
            log_message "SUCCÈS: $script_name terminé avec succès"
            return 0
        else
            log_message "ERREUR: Échec de l'exécution de $script_name"
            return 1
        fi
    else
        log_message "ERREUR: Script $script_name introuvable à l'emplacement: $script_path"
        return 1
    fi
}

# Début du script principal
log_message "=============================================="
log_message "DÉBUT DE L'ORCHESTRATION DES SCRIPTS"
log_message "=============================================="

# 1. Exécution du scraping (premier)
log_message "PHASE 1: SCRAPING DES DONNÉES"
run_script "run_all_scraping.sh" "${BASE_DIR}/run_all_scraping.sh"

# Pause entre les phases
sleep 5

# 2. Exécution de l'insertion des données (deuxième)
log_message "PHASE 2: INSERTION DES DONNÉES"
run_script "run_all_insert.sh" "${BASE_DIR}/run_all_insert.sh"

# Pause entre les phases
sleep 5

# 3. Exécution du machine learning (troisième)
log_message "PHASE 3: TRAITEMENT MACHINE LEARNING"
run_script "run_all_ml.sh" "${BASE_DIR}/run_all_ml.sh"

# Résumé final
log_message "=============================================="
log_message "RÉSUMÉ DE L'EXÉCUTION"
log_message "Log principal: $LOGFILE_MAIN"
log_message "Log scraping: ${BASE_DIR}/run_all_scraping.log"
log_message "Log insertion: ${BASE_DIR}/run_all_insert.log"
log_message "Log ML: ${BASE_DIR}/run_all_ml.log"
log_message "=============================================="

log_message "ORCHESTRATION TERMINÉE - Vérifiez les logs pour les détails"
