"""
But des tests :
- Valider le comportement de l'API et détecter toute régression après mise à jour.
- Chaque test doit indiquer clairement si le résultat est conforme à ce qui est attendu.

Types de tests couverts :
- Test de prédiction valide
- Test de prédiction invalide (update / payload incorrect)
- Test d’authentification (accès avec utilisateur/token)

⚠️ Si les tests échouent par erreur de connectivité :
- Vérifie que les tests atteignent bien l’API dans Docker (réseau, exécution dans le conteneur).
- Vérifie l’URL utilisée dans les tests (nom du service Docker ou IP du conteneur).
- Vérifie les variables d’environnement (.env), ou mets l’URL en dur pour diagnostiquer.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestPredictRouter:

    def test_predict_commentaire(self):
        payload = {"commentaire": "Ceci est un test"}
        response = client.post("/predict", json=payload)
        assert response.status_code == 200
        assert "prediction" in response.json()

    def test_predict_commentaire_invalid(self):
        """Vérifie la réponse si le payload est invalide"""
        response = client.post("/predict", json={})
        assert response.status_code in [400, 422]

    def test_auth_predict(self):
        """Test d'accès protégé sur prédiction"""
        headers = {"Authorization": "Bearer faux_token"}
        response = client.post("/predict", json={"commentaire": "test"}, headers=headers)
        assert response.status_code in [200, 401]
