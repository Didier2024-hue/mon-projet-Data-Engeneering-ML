#!/bin/bash

# Script pour arrêter le serveur MLflow
echo "🛑 Arrêt du serveur MLflow..."

# Trouver le PID du processus MLflow
MLFLOW_PID=$(ps aux | grep "mlflow server" | grep -v grep | awk '{print $2}')

if [ -z "$MLFLOW_PID" ]; then
    echo "✅ Aucun serveur MLflow en cours d'exécution"
else
    echo "📋 PID du serveur MLflow trouvé: $MLFLOW_PID"
    
    # Arrêt propre du processus
    kill -TERM $MLFLOW_PID
    
    # Attendre un peu que le processus s'arrête
    sleep 2
    
    # Vérifier si le processus est toujours actif
    if ps -p $MLFLOW_PID > /dev/null; then
        echo "⚠️  Arrêt normal échoué, tentative de kill forcé..."
        kill -KILL $MLFLOW_PID
        sleep 1
    fi
    
    # Vérification finale
    if ps aux | grep "mlflow server" | grep -v grep > /dev/null; then
        echo "❌ Impossible d'arrêter le serveur MLflow"
        exit 1
    else
        echo "✅ Serveur MLflow arrêté avec succès"
    fi
fi

# Optionnel: Vérifier aussi les processus sur le port 5000
PORT_PID=$(lsof -ti:5000)
if [ -n "$PORT_PID" ]; then
    echo "🧹 Nettoyage des processus sur le port 5000: $PORT_PID"
    kill -9 $PORT_PID 2>/dev/null
fi

echo "🎯 Opération terminée"
