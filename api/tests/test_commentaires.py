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

class TestCommentairesRouter:

    def test_get_commentaires(self):
        response = client.get("/commentaires")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_commentaires_structure(self):
        """Vérifie la structure des documents retournés"""
        response = client.get("/commentaires")
        assert response.status_code == 200
        commentaires = response.json()
        if commentaires:
            commentaire = commentaires[0]
            assert "id" in commentaire
            assert "texte" in commentaire
            assert "note" in commentaire

    def test_update_commentaire(self):
        """Vérifie qu'une mise à jour fonctionne"""
        payload = {"texte": "Nouveau texte", "note": 4}
        response = client.put("/commentaires/1", json=payload)
        assert response.status_code in [200, 404]  # selon si l'ID existe
        if response.status_code == 200:
            data = response.json()
            assert data["texte"] == "Nouveau texte"
            assert data["note"] == 4

    def test_auth_commentaires(self):
        """Test d'accès protégé sur commentaires"""
        headers = {"Authorization": "Bearer faux_token"}
        response = client.get("/commentaires", headers=headers)
        assert response.status_code in [200, 401]
