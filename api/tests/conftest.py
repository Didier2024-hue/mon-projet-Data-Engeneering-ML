import pytest
from fastapi.testclient import TestClient
from main import app

# Importer le routeur export uniquement pour les tests
try:
    from routers import export
    app.include_router(export.router)
except ImportError:
    pass

@pytest.fixture(scope="session")
def client():
    """Client FastAPI pour tous les tests."""
    return TestClient(app)
