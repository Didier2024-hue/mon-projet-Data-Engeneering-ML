# /home/datascientest/cde/api/scripts/pages/api_client.py
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv("/home/datascientest/cde/api/.env.api")

# Configuration de l'API
API_HOST = os.getenv("API_HOST", "api")
API_PORT = int(os.getenv("API_PORT", 8000))
API_URL = f"http://{API_HOST}:{API_PORT}"

def get_societes(limit=100):
    try:
        response = requests.get(f"{API_URL}/societes/", params={"limit": limit})
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        return []

def get_last_comments(societe_id=None, limit=100, skip=0):
    try:
        params = {"limit": limit, "skip": skip}
        if societe_id:
            params["societe_id"] = societe_id
        
        response = requests.get(f"{API_URL}/commentaires/last", params=params)
        return response.json() if response.status_code == 200 else {"comments": []}
    except Exception as e:
        return {"comments": []}

def get_societes_with_notes(limit=1000):
    try:
        response = requests.get(f"{API_URL}/commentaires/societes", params={"limit": limit})
        return response.json() if response.status_code == 200 else {"societes": []}
    except Exception as e:
        return {"societes": []}

def get_top_avis(societe_id=None, limit=10, positif=True):
    try:
        params = {"limit": limit, "positif": positif}
        if societe_id:
            params["societe_id"] = societe_id
        
        response = requests.get(f"{API_URL}/commentaires/top_avis", params=params)
        return response.json() if response.status_code == 200 else {"top_avis": []}
    except Exception as e:
        return {"top_avis": []}

def predict_note(text):
    try:
        response = requests.post(f"{API_URL}/predict/note", json={"text": text})
        return response.json() if response.status_code == 200 else {"error": "Erreur de prédiction"}
    except Exception as e:
        return {"error": "Impossible de se connecter à l'API"}

def predict_sentiment(text):
    try:
        response = requests.post(f"{API_URL}/predict/sentiment", json={"text": text})
        return response.json() if response.status_code == 200 else {"error": "Erreur de prédiction"}
    except Exception as e:
        return {"error": "Impossible de se connecter à l'API"}

def export_comments(societe_id, n_commentaires=50, formats=["csv"]):
    try:
        data = {
            "societe_id": societe_id,
            "n_commentaires": n_commentaires,
            "formats": formats
        }
        response = requests.post(f"{API_URL}/export/", json=data)
        return response.json() if response.status_code == 200 else {"error": "Erreur d'export"}
    except Exception as e:
        return {"error": "Impossible de se connecter à l'API"}