# routers/commentaires.py
import re
from fastapi import APIRouter, Query, Depends
from routers.auth import guard
from services.mongo_service import get_last_comments, list_societes, db
from enum import Enum

router = APIRouter(prefix="/commentaires", tags=["Commentaires"])

# -----------------------
# Enum des sociétés connues (pour Swagger)
# -----------------------
class SocieteEnum(str, Enum):
    temu = "temu.com"
    tesla = "tesla.com"
    chronopost = "chronopost.fr"
    vinted = "vinted.fr"

# -----------------------
# Derniers commentaires
# (public en AUTH_MODE=off/partial, privé en AUTH_MODE=full)
# -----------------------
@router.get("/last")
def fetch_last_comments(
    societe_id: SocieteEnum | None = Query(
        None,
        description="Choisir une société dans la liste"
    ),
    limit: int = Query(100, ge=1, le=1000, description="Nombre max de commentaires à retourner"),
    skip: int = Query(0, ge=0, description="Décalage pour la pagination"),
    user=Depends(guard("full_only")),  # 🔒 activé uniquement si AUTH_MODE=full
):
    """
    Retourne les derniers commentaires enregistrés dans MongoDB.
    """
    return {"comments": get_last_comments(societe_id=societe_id, limit=limit, skip=skip)}

# -----------------------
# Liste des sociétés
# (public en AUTH_MODE=off/partial, privé en AUTH_MODE=full)
# -----------------------
@router.get("/societes")
def fetch_societes(
    limit: int = Query(1000, ge=1, le=5000),
    user=Depends(guard("full_only")),  # 🔒 activé uniquement si AUTH_MODE=full
):
    """
    Retourne la liste des sociétés avec leur note globale (depuis collection 'societe').
    """
    return {"societes": list_societes(limit=limit)}

# -----------------------
# Top Avis
# (public en AUTH_MODE=off/partial, privé en AUTH_MODE=full)
# -----------------------
@router.get("/top_avis")
def fetch_top_avis(
    societe_id: str | None = Query(
        None,
        description="Filtre société: accepte 'temu' ou 'temu.com', etc."
    ),
    limit: int = Query(10, ge=1, le=100, description="Nombre d'avis à retourner"),
    positif: bool = Query(True, description="True = meilleurs avis (note=5), False = pires avis (note=1)"),
    user=Depends(guard("full_only")),  # 🔒 requis seulement si AUTH_MODE=full
):
    """
    Retourne les avis les plus positifs/négatifs.
    - Supporte note stockée en int (note) ou texte (note_commentaire).
    - Fait un filtrage strict (5/1), puis fallback par tri si aucun résultat.
    """
    collection = db["avis_trustpilot"]

    # ----- Filtre société (souple) -----
    base_query = {}
    if societe_id:
        pat = re.escape(societe_id.strip())
        base_query["$or"] = [
            {"id_societe": {"$regex": pat, "$options": "i"}},
            {"societe_nom": {"$regex": pat, "$options": "i"}},
        ]

    # ----- Filtre de note strict (5 ou 1) -----
    target = 5 if positif else 1
    note_or = [
        {"note": target},  # note entière
        {"note_commentaire": target},  # au cas où ce soit enregistré en int
        {"note_commentaire": {"$regex": rf"^\s*{target}\b", "$options": "i"}},  # texte "5" / "1"
    ]
    strict_query = {"$and": [base_query, {"$or": note_or}]} if base_query else {"$or": note_or}

    sort_order = -1 if positif else 1
    cursor = (
        collection.find(strict_query)
        .sort([("note", sort_order), ("note_commentaire", sort_order)])
        .limit(limit)
    )
    docs = list(cursor)

    # ----- Fallback si aucun résultat : on relâche le filtre de note, on garde le tri -----
    if not docs:
        cursor = (
            collection.find(base_query or {})
            .sort([("note", sort_order), ("note_commentaire", sort_order)])
            .limit(limit)
        )
        docs = list(cursor)

    avis = [
        {
            "id": str(d.get("_id")),
            "auteur": d.get("auteur"),
            "commentaire": d.get("commentaire"),
            "note": (
                d.get("note_commentaire")
                if d.get("note_commentaire") not in (None, "")
                else d.get("note")
            ),
            "date": d.get("date"),
            "societe": d.get("societe_nom") or d.get("id_societe"),
        }
        for d in docs
    ]
    return {"top_avis": avis}

# -----------------------
# Liste de commentaires factices (pour tests unitaires)
# (laisse-le public)
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
