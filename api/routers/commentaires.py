from fastapi import APIRouter, Query
from services.mongo_service import get_last_comments, list_societes, db

router = APIRouter(prefix="/commentaires", tags=["Commentaires"])

# -----------------------
# Derniers commentaires
# -----------------------
@router.get("/last")
def fetch_last_comments(
    societe_id: str | None = Query(None, description="Filtrer par identifiant ou nom de société"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre max de commentaires à retourner"),
    skip: int = Query(0, ge=0, description="Décalage pour la pagination")
):
    """
    Retourne les derniers commentaires enregistrés dans MongoDB.
    """
    return {"comments": get_last_comments(societe_id=societe_id, limit=limit, skip=skip)}

# -----------------------
# Liste des sociétés
# -----------------------
@router.get("/societes")
def fetch_societes(limit: int = Query(1000, ge=1, le=5000)):
    """
    Retourne la liste des sociétés avec leur note globale (depuis collection 'societe').
    """
    return {"societes": list_societes(limit=limit)}

# -----------------------
# Top Avis
# -----------------------
@router.get("/top_avis")
def fetch_top_avis(
    societe_id: str | None = Query(None, description="Filtrer par société"),
    limit: int = Query(10, ge=1, le=100, description="Nombre d'avis à retourner"),
    positif: bool = Query(True, description="True = meilleurs avis (note=5), False = pires avis (note=1)")
):
    """
    Retourne les avis les plus positifs ou négatifs pour une société.
    """
    collection = db["avis_trustpilot"]

    query = {}
    if societe_id:
        query["$or"] = [
            {"id_societe": {"$regex": societe_id, "$options": "i"}},
            {"societe_nom": {"$regex": societe_id, "$options": "i"}},
        ]

    query["note_commentaire"] = "5" if positif else "1"

    try:
        cursor = (
            collection.find(query)
            .sort("date_chargement", -1)
            .limit(limit)
        )

        avis = [
            {
                "id": str(d["_id"]),
                "auteur": d.get("auteur"),
                "commentaire": d.get("commentaire"),
                "note": d.get("note_commentaire"),
                "date": d.get("date"),
                "societe": d.get("societe_nom"),
            }
            for d in cursor
        ]

        return {"top_avis": avis}

    except Exception as e:
        return {"error": str(e)}

# -----------------------
# Liste de commentaires factices (pour tests unitaires)
# -----------------------
@router.get("/")
async def get_commentaires():
    """
    Endpoint factice ajouté pour les tests unitaires.
    Retourne une liste statique de commentaires.
    """
    return [
        {"id": 1, "texte": "Super service", "note": 5},
        {"id": 2, "texte": "Pas terrible", "note": 2},
    ]
