#!/bin/bash

echo "========================================"
echo "     🔍 DIAGNOSTIC COMPLET DE LA VM"
echo "========================================"
echo ""

##############################
# 1) ETAT DU DISQUE
##############################
echo "📦 Espace disque :"
df -h
echo ""
echo "----------------------------------------"

##############################
# 2) MEMOIRE DETAILLEE
##############################
echo "🧠 Mémoire (RAM + Swap) :"
/usr/bin/free -h
echo ""
echo "----------------------------------------"

##############################
# 3) CPU + RAM + PROCESSUS
##############################
echo "💻 Top (CPU + RAM + Process gourmands) :"
top -b -n 1 | head -n 30
echo ""
echo "----------------------------------------"

##############################
# 4) DOCKER : CONTAINERS ACTIFS
##############################
echo "�� Containers Docker actifs :"
docker ps
echo ""
echo "----------------------------------------"

##############################
# 5) DOCKER : TOUS LES CONTAINERS
##############################
echo "�� Tous les containers (actifs et arrêtés) :"
docker ps -a
echo ""
echo "----------------------------------------"

##############################
# 6) DOCKER : RESSOURCES UTILISÉES
##############################
echo "📊 Ressources des containers Docker :"
docker stats --no-stream
echo ""
echo "----------------------------------------"

##############################
# 7) PROCESSUS LIÉS AUX OUTILS DATA/DEVOPS
##############################
echo "🔎 Processus airflow|celery|postgres|mongo|grafana|prometheus|node_exporter|uvicorn|fastapi|streamlit|mlflow|docker|python3|python :"
echo ""
ps aux | grep -E "airflow|celery|postgres|mongo|grafana|prometheus|node_exporter|uvicorn|fastapi|streamlit|mlflow|docker|python3|python" \
       | grep -v grep \
       | sort -k4,4nr
echo "----------------------------------------"

##############################
# 8) SERVICES SYSTEME
##############################
echo "🟢 Services système actifs :"
systemctl --type=service --state=running
echo ""
echo "----------------------------------------"

##############################
# 9) VERSIONS UTILES
##############################
echo "🔧 Versions (Docker, Compose, Python, PostgreSQL, etc.) :"
docker --version
docker compose version
python3 --version
psql --version 2>/dev/null || echo "psql non installé"
echo ""
echo "----------------------------------------"

echo "✅ DIAGNOSTIC TERMINÉ."

