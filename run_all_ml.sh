#!/bin/bash

LOGFILE_ML="/home/datascientest/cde/run_all_ml.log"

echo "Lancement de snapshot_data.py" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/preprocess/snapshot_data.py 2>&1 | tee -a "LOGFILE_ML"

echo "Lancement de sentiment_analysis.py" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/preprocess/sentiment_analysis.py 2>&1 | tee -a "$LOGFILE_ML"

echo "Lancement de clean_data.py" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/preprocess/clean_data.py 2>&1 | tee -a "$LOGFILE_ML"

echo "Lancement de preprocess_clean_avis.py" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/preprocess/preprocess_clean_avis.py 2>&1 | tee -a "$LOGFILE_ML"

echo "Lancement du modele de prédiction" | tee -a "$LOGFILE_ML"
python3 /home/datascientest/cde/scripts/models/train_dual_models.py 2>&1 | tee -a "$LOGFILE_ML"

echo "Tous les scripts sont terminés." | tee -a "$LOGFILE_ML"