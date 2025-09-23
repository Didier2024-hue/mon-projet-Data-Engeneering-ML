#!/bin/bash

LOGFILE_INSERT="/home/datascientest/cde/run_all_insert.log"

echo "Lancement de cde_insert_wiki.py" | tee -a "$LOGFILE_INSERT"
python3 /home/datascientest/cde/scripts/insert/cde_insert_wiki.py  2>&1 | tee -a "$LOGFILE_INSERT"

echo "Lancement de insert_postgre.py" | tee -a "$LOGFILE_INSERT"
python3 /home/datascientest/cde/scripts/insert/insert_postgre.py 2>&1 | tee -a "$LOGFILE_INSERT"

echo "Lancement de insert_mongodb.py" | tee -a "$LOGFILE_INSERT"
python3 /home/datascientest/cde/scripts/insert/insert_mongodb.py 2>&1 | tee -a "$LOGFILE_INSERT"

echo "Lancement de l'insert dans mongodb et postgre" | tee -a "$LOGFILE_INSERT"
