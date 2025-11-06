# routers/commentaires.py
import re
import os
from enum import Enum
from typing import Optional, List, Dict
from fastapi import APIRouter, Query, Depends, HTTPException
from routers.auth import guard
from services.mongo_service import get_last_comments, list_societes, db
from bson import ObjectId
from re import findall, escape

# -----------------------
# Router principal
# -----------------------
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
# -----------------------
@router.get("/last")
def fetch_last_comments(
    societe_id: SocieteEnum | None = Query(None, description="Choisir une société"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre max de commentaires à retourner"),
    skip: int = Query(0, ge=0, description="Décalage pour la pagination"),
    user=Depends(guard("full_only")),  # 🔒 activé uniquement si AUTH_MODE=full
):
    """Retourne les derniers commentaires enregistrés dans MongoDB."""
    return {"comments": get_last_comments(societe_id=societe_id, limit=limit, skip=skip)}

# -----------------------
# Liste des sociétés
# -----------------------
@router.get("/societes")
def fetch_societes(
    limit: int = Query(1000, ge=1, le=5000),
    user=Depends(guard("full_only")),
):
    """Retourne la liste des sociétés avec leur note globale."""
    return {"societes": list_societes(limit=limit)}

# -----------------------
# Top Avis
# -----------------------
@router.get("/top_avis")
def fetch_top_avis(
    societe_id: str | None = Query(None, description="Filtre société: accepte 'temu' ou 'temu.com', etc."),
    limit: int = Query(10, ge=1, le=100, description="Nombre d'avis à retourner"),
    positif: bool = Query(True, description="True = meilleurs avis (note=5), False = pires avis (note=1)"),
    user=Depends(guard("full_only")),
):
    """Retourne les avis les plus positifs/négatifs."""
    collection = db["avis_trustpilot"]

    # ----- Filtre société -----
    base_query: Dict = {}
    if societe_id:
        pat = re.escape(societe_id.strip())
        base_query["$or"] = [
            {"id_societe": {"$regex": pat, "$options": "i"}},
            {"societe_nom": {"$regex": pat, "$options": "i"}},
        ]

    # ----- Filtre de note -----
    target = 5 if positif else 1
    note_or = [
        {"note": target},
        {"note_commentaire": target},
        {"note_commentaire": {"$regex": rf"^\s*{target}\b", "$options": "i"}},
    ]
    strict_query = {"$and": [base_query, {"$or": note_or}]} if base_query else {"$or": note_or}

    sort_order = -1 if positif else 1
    cursor = collection.find(strict_query).sort(
        [("note", sort_order), ("note_commentaire", sort_order)]
    ).limit(limit)

    docs = list(cursor)
    if not docs:
        cursor = collection.find(base_query or {}).sort(
            [("note", sort_order), ("note_commentaire", sort_order)]
        ).limit(limit)
        docs = list(cursor)

    avis = [
        {
            "id": str(d.get("_id")),
            "auteur": d.get("auteur"),
            "commentaire": d.get("commentaire"),
            "note": d.get("note_commentaire") or d.get("note"),
            "date": d.get("date"),
            "societe": d.get("societe_nom") or d.get("id_societe"),
        }
        for d in docs
    ]
    return {"top_avis": avis}

# -----------------------
# Recherche par mots/phrases (+ filtre société)
# -----------------------
@router.get("/search")
def search_commentaires(
    q: str = Query(..., description='Un ou plusieurs mots/phrases. Mettez une phrase entre guillemets pour une recherche exacte, ex: "Plus jamais".'),
    societe: str | None = Query(None, description="Ex: temu, temu.com, vinted, vinted.fr"),
    limit: int = Query(50, ge=1, le=1000),
    match_all: bool = Query(False, description="True = tous les tokens doivent être présents (ET). False = au moins un (OU)."),
):
    """
    Recherche flexible insensible à la casse dans 'commentaire'.
    - q peut contenir des mots et/ou des phrases entre guillemets
    - match_all contrôle la combinaison AND/OR des tokens
    - filtre optionnel par société (id_societe OU societe_nom)
    """
    collection = db["avis_trustpilot"]

    q = (q or "").strip()
    if not q:
        return {"count": 0, "results": [], "info": "Aucun critère"}

    # Extraire tokens : "phrase exacte" OU mots isolés
    tokens: List[str] = []
    for phrase, word in findall(r'"([^"]+)"|(\S+)', q):
        token = (phrase or word).strip()
        if token:
            tokens.append(token)

    # Construire clause texte (regex escape pour éviter surprises)
    subconds = [{"commentaire": {"$regex": escape(t), "$options": "i"}} for t in tokens] or [
        {"commentaire": {"$regex": escape(q), "$options": "i"}}
    ]
    text_clause = {"$and": subconds} if match_all and len(subconds) > 1 else {"$or": subconds}

    # Filtre société (souple)
    final_query: Dict
    if societe:
        base = societe.strip()
        company_id = base.split('.')[0]  # "temu.com" -> "temu"
        societe_filter = {
            "$or": [
                {"id_societe": {"$regex": company_id, "$options": "i"}},
                {"societe_nom": {"$regex": base,        "$options": "i"}},
            ]
        }
        final_query = {"$and": [text_clause, societe_filter]}
    else:
        final_query = text_clause

    # Projection utile
    projection = {
        "_id": 1, "auteur": 1, "commentaire": 1, "date": 1,
        "id_societe": 1, "societe_nom": 1, "note": 1, "note_commentaire": 1,
        "url_page": 1,
    }

    cursor = db["avis_trustpilot"].find(final_query, projection).limit(limit)
    docs: List[Dict] = []
    for d in cursor:
        d["_id"] = str(d["_id"])
        docs.append(d)

    return {"count": len(docs), "results": docs, "query": final_query}

# -----------------------
# Commentaire par ID (éviter conflit avec /search)
# -----------------------
@router.get("/id/{comment_id}")
def get_commentaire_by_id(comment_id: str):
    collection = db["avis_trustpilot"]

    if not ObjectId.is_valid(comment_id):
        raise HTTPException(status_code=404, detail="ID invalide")

    doc = collection.find_one({"_id": ObjectId(comment_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Commentaire non trouvé")

    doc["_id"] = str(doc["_id"])
    return doc

# -----------------------
# Tous les commentaires (sans limite)
# -----------------------
@router.get("/full")
def fetch_all_comments(
    societe_id: str = Query(..., description="Nom ou domaine de la société (ex: chronopost.fr)"),
    user=Depends(guard("full_only")),
):
    """
    Retourne tous les commentaires d'une société (sans limite, pour analyses / dashboard).
    ⚠️ À utiliser uniquement côté back-office ou dashboard, pas en front public.
    """
    collection = db["avis_trustpilot"]

    query = {
        "$or": [
            {"societe_nom": {"$regex": societe_id, "$options": "i"}},
            {"id_societe": {"$regex": societe_id, "$options": "i"}},
        ]
    }

    cursor = collection.find(query)
    docs = []
    for d in cursor:
        d["_id"] = str(d["_id"])  # conversion ObjectId -> str
        docs.append(d)

    return {"comments": docs, "count": len(docs)}


# -----------------------
# Liste de commentaires factices (pour tests)
# -----------------------
@router.get("/")
async def get_commentaires():
    """Endpoint factice pour tests unitaires."""
    return [
        {"id": 1, "texte": "Super service", "note": 5},
        {"id": 2, "texte": "Pas terrible", "note": 2},
    ]
