from fastapi import APIRouter, Query
from services.mongo_service import list_societes

router = APIRouter(prefix="/societes", tags=["Sociétés"])

@router.get("/")
def fetch_societes(limit: int = Query(1000, ge=1, le=5000)):
    societes = list_societes(limit=limit)

    for soc in societes:
        soc["secteur"] = soc.get("secteur", "inconnu")

    # ✅ Retourner directement une liste
    return societes
