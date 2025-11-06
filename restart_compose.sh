#!/bin/bash
set -e  # Stopper si une commande échoue

echo "🧹 Nettoyage des fichiers Python compilés..."
find ./api -name "*.pyc" -delete || true
find ./api -name "__pycache__" -type d -exec rm -rf {} + || true

# Vérifier et activer le swap si nécessaire
if ! swapon --show | grep -q "swapfile"; then
  echo "💾 Activation du swap..."
  sudo swapon /home/datascientest/cde/swapfile || echo "⚠️ Impossible d'activer le swap (déjà actif ?)"
else
  echo "💾 Swap déjà actif."
fi

# Vérifier l'espace disque
echo "💽 Vérification de l'espace disque..."
df -h /home/datascientest/cde | tail -n 1

# Arrêter les containers
echo "📦 Arrêt des containers Docker..."
docker-compose down

# Reconstruire les images critiques (API + MLflow)
echo "🔧 Reconstruction des services critiques..."
docker-compose build api mlflow

# Relancer les containers
echo "🚀 Démarrage des containers..."
docker-compose up -d

# Attendre que MLflow devienne healthy (jusqu’à 3 minutes max)
echo "⏳ Vérification de l’état de MLflow..."
for i in {1..18}; do
  STATUS=$(docker inspect -f '{{.State.Health.Status}}' mlflow-cde 2>/dev/null || echo "unknown")
  if [ "$STATUS" == "healthy" ]; then
    echo "✅ MLflow est prêt !"
    break
  fi
  echo "🕐 Attente... (tentative $i/18)"
  sleep 10
done

# Afficher le résumé
echo "📊 État des conteneurs :"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo "✅ Redémarrage complet terminé avec succès."
