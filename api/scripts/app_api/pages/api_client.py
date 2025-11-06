# /home/datascientest/cde/api/scripts/pages/api_client.py
import requests
import os
from dotenv import load_dotenv

# =======================
# Chargement de la configuration
# =======================
load_dotenv()  # On charge l'environnement (dans le conteneur)

API_HOST = os.getenv("API_HOST", "fastapi-cde")
API_PORT = int(os.getenv("API_PORT", 8000))
API_URL = f"http://{API_HOST}:{API_PORT}"

print(f"[api_client] ✅ API_URL configurée sur : {API_URL}")

# =======================
# Auth (JWT)
# =======================
_ACCESS_TOKEN: str | None = None


def set_token(token: str | None) -> None:
    """Stocke (ou efface) le token en mémoire."""
    global _ACCESS_TOKEN
    _ACCESS_TOKEN = token


def get_token() -> str | None:
    return _ACCESS_TOKEN


def is_authenticated() -> bool:
    return _ACCESS_TOKEN is not None


def _auth_headers() -> dict:
    """Ajoute le header Authorization si un token est connu."""
    return {"Authorization": f"Bearer {_ACCESS_TOKEN}"} if _ACCESS_TOKEN else {}


# =======================
# Auth API
# =======================
def login(username: str, password: str) -> dict:
    """Auth: POST /auth/login et stocke le JWT si succès."""
    try:
        resp = requests.post(
            f"{API_URL}/auth/login",
            json={"username": username, "password": password},
            timeout=3,
        )
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
    """Déconnexion côté client: on efface le token."""
    set_token(None)


# =======================
# Helper pour uniformiser les réponses
# =======================
def _json_or_auth_required(resp, default_ok):
    if resp.status_code == 200:
        try:
            return resp.json()
        except Exception:
            return default_ok
    if resp.status_code in (401, 403):
        return {"error": "auth_required", "status_code": resp.status_code}
    try:
        return resp.json()
    except Exception:
        return {"error": resp.text or "Erreur API", "status_code": resp.status_code}


# =======================
# Appels API
# =======================
def get_societes(limit=100):
    try:
        resp = requests.get(
            f"{API_URL}/societes/",
            params={"limit": limit},
            headers=_auth_headers(),
            timeout=3,
        )
        return _json_or_auth_required(resp, [])
    except Exception:
        return []


def get_last_comments(societe_id=None, limit=100, skip=0):
    try:
        params = {"limit": limit, "skip": skip}
        if societe_id:
            params["societe_id"] = societe_id
        resp = requests.get(
            f"{API_URL}/commentaires/last",
            params=params,
            headers=_auth_headers(),
            timeout=3,
        )
        return _json_or_auth_required(resp, {"comments": []})
    except Exception:
        return {"comments": []}


def get_societes_with_notes(limit=1000):
    try:
        resp = requests.get(
            f"{API_URL}/commentaires/societes",
            params={"limit": limit},
            headers=_auth_headers(),
            timeout=3,
        )
        return _json_or_auth_required(resp, {"societes": []})
    except Exception:
        return {"societes": []}


def get_top_avis(societe_id=None, limit=10, positif=True):
    try:
        params = {"limit": limit, "positif": positif}
        if societe_id:
            params["societe_id"] = societe_id
        resp = requests.get(
            f"{API_URL}/commentaires/top_avis",
            params=params,
            headers=_auth_headers(),
            timeout=3,
        )
        return _json_or_auth_required(resp, {"top_avis": []})
    except Exception:
        return {"top_avis": []}


def predict_note(text: str):
    try:
        payload = {"commentaire": text, "text": text}
        resp = requests.post(
            f"{API_URL}/predict/note",
            json=payload,
            headers=_auth_headers(),
            timeout=3,
        )
        return _json_or_auth_required(resp, {"error": "Erreur de prédiction"})
    except Exception:
        return {"error": "Impossible de se connecter à l'API"}


def predict_sentiment(text: str):
    try:
        payload = {"commentaire": text, "text": text}
        resp = requests.post(
            f"{API_URL}/predict/sentiment",
            json=payload,
            headers=_auth_headers(),
            timeout=3,
        )
        return _json_or_auth_required(resp, {"error": "Erreur de prédiction"})
    except Exception:
        return {"error": "Impossible de se connecter à l'API"}


# =======================
# Nouvelles routes "commentaires"
# =======================
def get_comment_by_id(comment_id: str):
    try:
        resp = requests.get(
            f"{API_URL}/commentaires/{comment_id}",
            headers=_auth_headers(),
            timeout=3,
        )
        return _json_or_auth_required(resp, {"error": "Commentaire introuvable"})
    except Exception:
        return {"error": "Impossible de se connecter à l'API"}


def search_comments(keyword: str, limit=20):
    try:
        resp = requests.get(
            f"{API_URL}/commentaires/search",
            params={"q": keyword, "limit": limit},
            headers=_auth_headers(),
            timeout=3,
        )
        return _json_or_auth_required(resp, {"results": []})
    except Exception:
        return {"results": []}
    
def get_all_comments(societe_id: str):
    """
    Récupère l'ensemble des avis pour une société via /commentaires/full
    """
    try:
        params = {"societe_id": societe_id}
        resp = requests.get(
            f"{API_URL}/commentaires/full",
            params=params,
            headers=_auth_headers(),
            timeout=10,
        )
        return _json_or_auth_required(resp, {"comments": []})
    except Exception as e:
        print(f"[get_all_comments] ❌ Erreur API : {e}")
        return {"comments": []}

