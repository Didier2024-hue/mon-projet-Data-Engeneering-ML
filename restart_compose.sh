#!/bin/bash
set -e

BASE_DIR="/home/datascientest/cde"
MONITORING_DIR="$BASE_DIR/monitoring"
AIRFLOW_DIR="$BASE_DIR/airflow"
SWAPFILE="$BASE_DIR/swapfile"

echo "🧹 Nettoyage des fichiers Python compilés..."

# Suppression normale
find "$BASE_DIR/api" -name "*.pyc" -delete 2>/dev/null || true
find "$BASE_DIR/api" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Détection de fichiers non supprimés -> sudo uniquement pour ceux-là
REMAINING_PYC=$(find "$BASE_DIR/api" -name "*.pyc" 2>/dev/null | wc -l)
if [ "$REMAINING_PYC" -gt 0 ]; then
  echo "⚠️  Certains fichiers .pyc nécessitent sudo pour être supprimés..."
  sudo find "$BASE_DIR/api" -name "*.pyc" -delete || true
  sudo find "$BASE_DIR/api" -name "__pycache__" -type d -exec rm -rf {} + || true
else
  echo "✔️  Aucun fichier .pyc résistant."
fi


# ------------------------------------------------------------------------
# SWAP (sudo autorisé uniquement ici)
# ------------------------------------------------------------------------
echo "💾 Vérification / activation du swap..."

if ! swapon --show | grep -q "$SWAPFILE"; then
  if [ -f "$SWAPFILE" ]; then
    echo "💾 Activation du swapfile..."
    sudo swapon "$SWAPFILE" || echo "⚠️ Impossible d'activer le swap."
  else
    echo "⚠️  Aucun swapfile trouvé à : $SWAPFILE"
  fi
else
  echo "✔️  Swap déjà actif."
fi


# ------------------------------------------------------------------------
# DISQUE
# ------------------------------------------------------------------------
echo "💽 Vérification de l’espace disque..."
df -h "$BASE_DIR" | tail -n 1


# ------------------------------------------------------------------------
# STOP STACK PRINCIPALE
# ------------------------------------------------------------------------
echo "📦 Arrêt des containers Docker (stack principale)..."
docker compose -f "$BASE_DIR/docker-compose.yml" down || true


# ------------------------------------------------------------------------
# MONITORING
# ------------------------------------------------------------------------
if [ -f "$MONITORING_DIR/docker-compose.monitoring.yml" ]; then
  echo "📦 Arrêt de la stack monitoring..."
  docker compose -f "$MONITORING_DIR/docker-compose.monitoring.yml" down || true
else
  echo "⚠️  Monitoring introuvable : $MONITORING_DIR/docker-compose.monitoring.yml"
fi


# ------------------------------------------------------------------------
# BUILD API + MLFLOW
# ------------------------------------------------------------------------
echo "🔧 Reconstruction API + MLflow..."
docker compose -f "$BASE_DIR/docker-compose.yml" build api mlflow


# ------------------------------------------------------------------------
# START STACK PRINCIPALE
# ------------------------------------------------------------------------
echo "🚀 Démarrage de la stack principale..."
docker compose -f "$BASE_DIR/docker-compose.yml" up -d


# ------------------------------------------------------------------------
# ATTENTE MLflow
# ------------------------------------------------------------------------
echo "⏳ Vérification de l'état de MLflow..."
for i in {1..18}; do
  STATUS=$(docker inspect -f '{{.State.Health.Status}}' mlflow-cde 2>/dev/null || echo "unknown")
  if [ "$STATUS" == "healthy" ]; then
    echo "✅ MLflow est prêt !"
    break
  fi
  echo "🕐 Attente... (tentative $i/18)... statut: $STATUS"
  sleep 10
done


# ------------------------------------------------------------------------
# MONITORING START
# ------------------------------------------------------------------------
if [ -f "$MONITORING_DIR/docker-compose.monitoring.yml" ]; then
  echo "📦 Démarrage Monitoring..."
  docker compose -f "$MONITORING_DIR/docker-compose.monitoring.yml" up -d
else
  echo "⚠️  Monitoring introuvable, skip"
fi


# ------------------------------------------------------------------------
# AIRFLOW
# ------------------------------------------------------------------------
if [ -d "$AIRFLOW_DIR" ]; then
  echo "📦 Démarrage Airflow..."
  docker compose -f "$AIRFLOW_DIR/docker-compose-airflow.yaml" up -d
else
  echo "⚠️  Répertoire Airflow introuvable : $AIRFLOW_DIR"
fi


# ------------------------------------------------------------------------
# DOCKER STATUS
# ------------------------------------------------------------------------
echo "📊 Conteneurs actifs :"
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"

echo "✅ Redémarrage complet terminé avec succès."
