#!/bin/bash

echo "Killing all CDE tasks..."

pkill -f run_all_scraping.sh
pkill -f run_all_insert.sh
pkill -f run_all_ml.sh

pkill -f snapshot_data.py
pkill -f clean_data.py
pkill -f preprocess_clean_avis.py
pkill -f sentiment_analysis.py
pkill -f train_dual_models.py

pkill -f "/home/datascientest/cde/cde_env"

echo "Done!"

