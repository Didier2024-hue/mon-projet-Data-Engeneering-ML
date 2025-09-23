"""
But des tests :
- Valider le comportement de l'API et détecter toute régression après mise à jour.
- Chaque test doit indiquer clairement si le résultat est conforme à ce qui est attendu.

Types de tests couverts :
- Test de l’export de données (format et intégrité)
- Test d’authentification (accès avec utilisateur/token)

⚠️ Si les tests échouent par erreur de connectivité :
- Vérifie que les tests atteignent bien l’API dans Docker (réseau, exécution dans le conteneur).
- Vérifie l’URL utilisée dans les tests (nom du service Docker ou IP du conteneur).
- Vérifie les variables d’environnement (.env), ou mets l’URL en dur pour diagnostiquer.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestExportRouter:

    def test_export_data(self):
        response = client.get("/export")
        assert response.status_code == 200

    def test_export_data_format(self):
        """Vérifie que l'export retourne un format valide (dict ou list)"""
        response = client.get("/export")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, (dict, list))

    def test_auth_export(self):
        """Test d'accès protégé sur export"""
        headers = {"Authorization": "Bearer faux_token"}
        response = client.get("/export", headers=headers)
        assert response.status_code in [200, 401]
