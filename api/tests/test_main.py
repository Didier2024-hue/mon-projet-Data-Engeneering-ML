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
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


