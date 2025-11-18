#!/bin/bash
set -e  # Stopper en cas d'erreur

echo "🧹 Nettoyage des fichiers Python compilés..."
find ./api -name "*.pyc" -delete || true
find ./api -name "__pycache__" -type d -exec rm -rf {} + || true

# Activer le swap si nécessaire
if ! swapon --show | grep -q "swapfile"; then
  echo "💾 Activation du swap..."
  sudo swapon /home/datascientest/cde/swapfile || echo "⚠️ Swap déjà actif ou introuvable"
else
  echo "💾 Swap déjà actif."
fi

# Vérifier espace disque
echo "💽 Vérification de l’espace disque..."
df -h /home/datascientest/cde | tail -n 1

echo "📦 Arrêt des containers Docker (stack principale)..."
docker compose down || true

echo "🔧 Reconstruction API + MLflow..."
docker compose build api mlflow

echo "🚀 Démarrage de la stack principale..."
docker compose up -d

# Attendre que MLflow soit healthy
echo "⏳ Vérification de l'état de MLflow..."
for i in {1..18}; do
  STATUS=$(docker inspect -f '{{.State.Health.Status}}' mlflow-cde 2>/dev/null || echo "unknown")
  if [ "$STATUS" == "healthy" ]; then
    echo "✅ MLflow est prêt !"
    break
  fi
  echo "🕐 Attente... (tentative $i/18)... statut actuel: $STATUS"
  sleep 10
done

echo "📦 Redémarrage d'Airflow..."
cd airflow
docker compose -f docker-compose-airflow.yaml up -d
cd ..

echo "📊 Conteneurs actifs :"
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"


echo "✅ Redémarrage complet terminé avec succès."
