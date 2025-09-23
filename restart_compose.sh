#!/bin/bash

# Stopper tous les containers
echo "📦 Arrêt des containers..."
docker-compose down

# Rebuild uniquement le service API
echo "🔧 Reconstruction du service API..."
docker-compose build api

# Relancer les containers en arrière-plan
echo "🚀 Démarrage des containers..."
docker-compose up -d

echo "✅ Opération terminée."

