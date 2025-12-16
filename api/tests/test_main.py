import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestMainAPI:

    def test_root(self):
        """Test de la route racine '/'"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Bienvenue sur l'API Trustpilot"}

    def test_health(self):
        """Test de la route '/health'"""
        response = client.get("/health")
        
        # Vérifier le code HTTP
        assert response.status_code == 200
        
        # Vérifier le format de la réponse
        data = response.json()
        
        # Vérifier les champs obligatoires
        assert "status" in data
        assert data["status"] == "healthy"  # Correspond à votre implémentation
        
        # Vérifier le timestamp (optionnel mais recommandé)
        assert "timestamp" in data
        
        # Option : vérifier le format ISO du timestamp
        import datetime
        try:
            datetime.datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
        except ValueError:
            pytest.fail("Timestamp n'est pas au format ISO valide")