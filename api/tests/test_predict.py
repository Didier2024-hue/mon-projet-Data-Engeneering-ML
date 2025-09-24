"""
Tests de l'API de prédiction :
- Vérifie les endpoints de prédiction de sentiment et de note
- Vérifie le comportement en cas de payload invalide
- Placeholder pour les tests d'authentification (sera utile quand la sécurité sera implémentée)
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestPredictRouter:

    def test_predict_sentiment(self):
        """Test prédiction de sentiment valide"""
        payload = {"commentaire": "Ceci est un test positif"}
        response = client.post("/predict/sentiment", json=payload)
        assert response.status_code == 200
        body = response.json()
        # L'API renvoie {"commentaire": "...", "sentiment": "..."}
        assert "sentiment" in body
        assert body["sentiment"] in ["positif", "négatif"]


    def test_predict_note(self):
        """Test prédiction de note valide"""
        payload = {"commentaire": "Ceci est un test"}
        response = client.post("/predict/note", json=payload)
        assert response.status_code == 200
        body = response.json()
        # L'API renvoie {"commentaire": "...", "note": ...}
        assert "note" in body
        assert isinstance(body["note"], (int, float))

    def test_predict_sentiment_invalid(self):
        """Vérifie la réponse si le payload est invalide"""
        response = client.post("/predict/sentiment", json={})
        # FastAPI + Pydantic retourne 422 en cas de schéma manquant
        assert response.status_code == 422

    def test_auth_predict(self):
        """Test d'accès protégé sur prédiction (placeholder, à revoir quand la sécurité sera implémentée)"""
        headers = {"Authorization": "Bearer faux_token"}
        response = client.post("/predict/sentiment", json={"commentaire": "test"}, headers=headers)
        # Pour l'instant, pas de sécurité => 200 attendu
        # Quand JWT sera activé, on attendra 401
        assert response.status_code in [200, 401]
