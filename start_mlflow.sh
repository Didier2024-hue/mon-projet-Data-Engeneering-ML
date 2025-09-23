#!/bin/bash
source ~/cde/cde_env/bin/activate

export MLFLOW_TRACKING_URI=postgresql+psycopg2://admin:admin@localhost/mlflow_db
export MLFLOW_ARTIFACT_ROOT=~/cde/mlruns

echo "🚀 Démarrage du serveur MLflow..."
mlflow ui \
  --backend-store-uri $MLFLOW_TRACKING_URI \
  --default-artifact-root $MLFLOW_ARTIFACT_ROOT \
  --host 0.0.0.0 \
  --port 5000 &

