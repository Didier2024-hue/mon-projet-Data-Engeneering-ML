from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient, ReturnDocument
from bson import ObjectId
import os

router = APIRouter(tags=["Default"])

# --------------------------
# Endpoints de base
# --------------------------
@router.get("/", summary="Root endpoint")
def root():
    return {"message": "Bienvenue sur l'API Trustpilot"}

@router.get("/health", summary="Healthcheck endpoint")
def health():
    return {"status": "ok"}

# --------------------------
# Connexion MongoDB
# --------------------------
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://admin:admin@mongo:27017/trustpilot?authSource=admin"
)

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
    db = client["trustpilot"]
    avis_collection = db["avis_trustpilot"]
    societe_collection = db["societe"]
except Exception as e:
    print("Erreur de connexion MongoDB :", e)
    avis_collection, societe_collection = None, None

# --------------------------
# Récupère un avis (sample)
# --------------------------
@router.get("/avis-sample", summary="Récupère un avis de Trustpilot")
def avis_sample():
    if avis_collection is None:
        raise HTTPException(status_code=500, detail="MongoDB non disponible")

    doc = avis_collection.find_one()
    if not doc:
        raise HTTPException(status_code=404, detail="Aucun avis trouvé")

    return {
        "id": str(doc["_id"]),
        "auteur": doc.get("auteur", "inconnu"),
        "societe": doc.get("societe_nom", ""),
        "note": doc.get("note_commentaire", ""),
        "commentaire": doc.get("commentaire", ""),
        "date": doc.get("date", "")
    }

# --------------------------
# Récupère une société (sample)
# --------------------------
@router.get("/societe-sample", summary="Récupère une société de Trustpilot")
def societe_sample():
    if societe_collection is None:
        raise HTTPException(status_code=500, detail="MongoDB non disponible")

    doc = societe_collection.find_one()
    if not doc:
        raise HTTPException(status_code=404, detail="Aucune société trouvée")

    return {
        "id": str(doc["_id"]),
        "nom": doc.get("nom", ""),
        "secteur": doc.get("secteur", ""),
        "note_globale": doc.get("note_globale", None),
        "total_avis": doc.get("total_avis", None),
    }

# --------------------------
# Mise à jour d'un avis
# --------------------------
class UpdateRequest(BaseModel):
    id: str
    commentaire: str

@router.put("/avis-update", summary="Met à jour le commentaire d'un avis Trustpilot")
def avis_update(request: UpdateRequest):
    if avis_collection is None:
        raise HTTPException(status_code=500, detail="MongoDB non disponible")

    try:
        object_id = ObjectId(request.id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID invalide (doit être un ObjectId MongoDB)")

    result = avis_collection.find_one_and_update(
        {"_id": object_id},
        {"$set": {"commentaire": request.commentaire}},
        return_document=ReturnDocument.AFTER
    )

    if not result:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    return {
        "id": str(result["_id"]),
        "auteur": result.get("auteur", "inconnu"),
        "note": result.get("note_commentaire", ""),
        "commentaire": result.get("commentaire", "")
    }
