# /home/datascientest/cde/api/scripts/pages/api_client.py
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement (.env.api)
load_dotenv("/home/datascientest/cde/api/.env.api")

# Configuration de l'API
API_HOST = os.getenv("API_HOST", "api")
API_PORT = int(os.getenv("API_PORT", 8000))
API_URL = f"http://{API_HOST}:{API_PORT}"

# =======================
# Auth (JWT)
# =======================
_ACCESS_TOKEN: str | None = None

def set_token(token: str | None) -> None:
    """Stocke (ou efface) le token en mémoire."""
    global _ACCESS_TOKEN
    _ACCESS_TOKEN = token

def get_token() -> str | None:
    """Retourne le token courant (ou None)."""
    return _ACCESS_TOKEN

def _auth_headers() -> dict:
    """Ajoute le header Authorization si un token est connu."""
    return {"Authorization": f"Bearer {_ACCESS_TOKEN}"} if _ACCESS_TOKEN else {}

def login(username: str, password: str) -> dict:
    """
    Authentifie l'utilisateur et stocke automatiquement le JWT.
    Retourne le dict de la réponse (ou {"error": "..."} en cas d'échec).
    """
    try:
        resp = requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("access_token")
            if token:
                set_token(token)
            return data
        return {"error": resp.text, "status_code": resp.status_code}
    except Exception as e:
        return {"error": f"Impossible de se connecter à l'API: {e}"}

def logout() -> None:
    """Efface le token (déconnexion côté client)."""
    set_token(None)

# =======================
# Appels API existants
# =======================
def get_societes(limit=100):
    try:
        # public en AUTH_MODE=off/partial ; privé en full_only (on peut envoyer le header sans risque)
        response = requests.get(f"{API_URL}/societes/", params={"limit": limit}, headers=_auth_headers())
        return response.json() if response.status_code == 200 else []
    except Exception:
        return []

def get_last_comments(societe_id=None, limit=100, skip=0):
    try:
        params = {"limit": limit, "skip": skip}
        if societe_id:
            params["societe_id"] = societe_id
        # public en AUTH_MODE=off/partial ; privé en full_only
        response = requests.get(f"{API_URL}/commentaires/last", params=params, headers=_auth_headers())
        return response.json() if response.status_code == 200 else {"comments": []}
    except Exception:
        return {"comments": []}

def get_societes_with_notes(limit=1000):
    try:
        # NB: cet endpoint est /commentaires/societes côté API
        response = requests.get(f"{API_URL}/commentaires/societes", params={"limit": limit}, headers=_auth_headers())
        return response.json() if response.status_code == 200 else {"societes": []}
    except Exception:
        return {"societes": []}

def get_top_avis(societe_id=None, limit=10, positif=True):
    try:
        params = {"limit": limit, "positif": positif}
        if societe_id:
            params["societe_id"] = societe_id
        # public en AUTH_MODE=off/partial ; privé en full_only
        response = requests.get(f"{API_URL}/commentaires/top_avis", params=params, headers=_auth_headers())
        return response.json() if response.status_code == 200 else {"top_avis": []}
    except Exception:
        return {"top_avis": []}

def predict_note(text: str):
    try:
        # ⚠️ L’API attend "commentaire" (cf. routers/predict.py)
        payload = {"commentaire": text, "text": text}  # "text" laissé pour compat amont, ignoré côté API
        response = requests.post(f"{API_URL}/predict/note", json=payload, headers=_auth_headers())
        return response.json() if response.status_code == 200 else {"error": response.text or "Erreur de prédiction"}
    except Exception:
        return {"error": "Impossible de se connecter à l'API"}

def predict_sentiment(text: str):
    try:
        # ⚠️ L’API attend "commentaire" (cf. routers/predict.py)
        payload = {"commentaire": text, "text": text}
        response = requests.post(f"{API_URL}/predict/sentiment", json=payload, headers=_auth_headers())
        return response.json() if response.status_code == 200 else {"error": response.text or "Erreur de prédiction"}
    except Exception:
        return {"error": "Impossible de se connecter à l'API"}

def export_comments(societe_id, n_commentaires=50, formats=["csv"]):
    try:
        data = {
            "societe_id": societe_id,
            "n_commentaires": n_commentaires,
            "formats": formats
        }
        # Protégé (sensitive) quand AUTH_MODE=partial/full
        response = requests.post(f"{API_URL}/export/", json=data, headers=_auth_headers())
        # Si l'API renvoie un fichier (StreamingResponse), .json() ne fonctionnera pas.
        # Ici on garde le comportement existant : on tente json() sinon on renvoie un statut.
        if "application/json" in (response.headers.get("Content-Type") or ""):
            return response.json()
        return {"status_code": response.status_code}
    except Exception:
        return {"error": "Impossible de se connecter à l'API"}
