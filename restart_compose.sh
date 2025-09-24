#!/bin/bash
set -e  # arrêter le script si une commande échoue

# Nettoyer les fichiers .pyc et __pycache__
echo "🧹 Nettoyage des fichiers Python compilés..."
find ./api -name "*.pyc" -delete || true
find ./api -name "__pycache__" -type d -exec rm -rf {} + || true

# Arrêter tous les containers
echo "📦 Arrêt des containers..."
docker-compose down

# Rebuild uniquement le service API
echo "🔧 Reconstruction du service API..."
docker-compose build api

# Relancer les containers en arrière-plan
echo "🚀 Démarrage des containers..."
docker-compose up -d

echo "✅ Opération terminée."
