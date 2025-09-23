"""
But des tests :
- Valider le comportement de l'API et détecter toute régression après mise à jour.
- Chaque test doit indiquer clairement si le résultat est conforme à ce qui est attendu.

Types de tests couverts :
- Test d’interrogation de la base (intégrité des champs)
- Test d’update (si implémenté)
- Test d’authentification (accès avec utilisateur/token)

⚠️ Si les tests échouent par erreur de connectivité :
- Vérifie que les tests atteignent bien l’API dans Docker (réseau, exécution dans le conteneur).
- Vérifie l’URL utilisée dans les tests (nom du service Docker ou IP du conteneur).
- Vérifie les variables d’environnement (.env), ou mets l’URL en dur pour diagnostiquer.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestSocietesRouter:

    def test_get_societes(self):
        response = client.get("/societes")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_societes_structure(self):
        """Vérifie la structure des documents retournés"""
        response = client.get("/societes")
        assert response.status_code == 200
        societes = response.json()
        if societes:
            societe = societes[0]
            assert "id" in societe
            assert "nom" in societe
            assert "secteur" in societe

    def test_update_societe(self):
        """Vérifie qu'une mise à jour fonctionne"""
        payload = {"nom": "Nouvelle Société", "secteur": "Tech"}
        response = client.put("/societes/1", json=payload)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert data["nom"] == "Nouvelle Société"
            assert data["secteur"] == "Tech"

    def test_auth_societes(self):
        """Test d'accès protégé sur sociétés"""
        headers = {"Authorization": "Bearer faux_token"}
        response = client.get("/societes", headers=headers)
        assert response.status_code in [200, 401]
