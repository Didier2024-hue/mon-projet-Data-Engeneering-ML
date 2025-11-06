import os
import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
import numpy as np
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# --- CONFIGURATION ---
BASE_DIR = "/home/datascientest/cde"
CSV_RESULTS = os.path.join(BASE_DIR, "data/processed/resultats_modeles.csv")
PKL_DIR = os.path.join(BASE_DIR, "data/model")
EXPERIMENT_NAME = "Trustpilot_Model_Results"

# --- Configuration MLflow pour PostgreSQL ---
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "postgresql://mlflow_user:admin@localhost/mlflow_db")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

# Fonction pour nettoyer le nom du modèle
def clean_model_name(name):
    """Nettoyer le nom du modèle pour MLflow"""
    forbidden_chars = ['/', ':', '.', '%', '"', "'", ' ']
    for char in forbidden_chars:
        name = name.replace(char, '_')
    return name.lower()

# --- Lecture des résultats ---
df = pd.read_csv(CSV_RESULTS)
print(f"✅ {len(df)} lignes de résultats chargées depuis {CSV_RESULTS}")

# --- Boucle sur les modèles ---
for _, row in df.iterrows():
    task = row["Tâche"].lower()
    model_name = row["Modèle"].lower()
    acc = row["Accuracy"]
    f1 = row["F1_score_macro"]

    # Nettoyer le nom pour MLflow
    clean_task = clean_model_name(task)
    clean_model = clean_model_name(model_name)
    run_name = f"{clean_task}_{clean_model}"
    
    # Correspondance avec fichiers pkl
    model_file = os.path.join(PKL_DIR, f"{model_name}_{task}.pkl")
    if not os.path.exists(model_file):
        print(f"❌ Fichier pkl non trouvé : {model_file}")
        continue

    # Charger le modèle
    try:
        model = joblib.load(model_file)
    except Exception as e:
        print(f"❌ Erreur chargement modèle {model_file}: {e}")
        continue

    # Préparer input example
    try:
        if hasattr(model, "coef_"):
            n_features = model.coef_.shape[1]
        elif hasattr(model, "n_features_in_"):
            n_features = model.n_features_in_
        else:
            n_features = 100  # Valeur par défaut
        input_example = pd.DataFrame(np.zeros((1, n_features)), columns=[f"f{i}" for i in range(n_features)])
    except Exception as e:
        input_example = None
        print(f"⚠ Impossible de créer input_example pour {run_name}: {e}")

    # Logging MLflow
    with mlflow.start_run(run_name=run_name):
        try:
            # Loguer le modèle avec nom nettoyé
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path=run_name,
                registered_model_name=run_name,
                input_example=input_example
            )
        except Exception as e:
            print(f"⚠ Erreur lors du log du modèle {run_name}: {e}")
            continue

        # Loguer les métriques
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_macro", f1)
        mlflow.log_param("task", task)
        mlflow.log_param("model_type", model_name)

        print(f"✅ Modèle logué : {run_name} | acc={acc:.4f} | f1={f1:.4f}")

print("🎯 Tous les modèles ont été traités!")
