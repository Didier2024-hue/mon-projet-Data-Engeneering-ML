# routers/societes.py
from fastapi import APIRouter, Query, Depends
from routers.auth import guard
from services.mongo_service import list_societes

router = APIRouter(prefix="/societes", tags=["Sociétés"])

@router.get("/")
def fetch_societes(
    limit: int = Query(1000, ge=1, le=5000),
    user=Depends(guard("full_only")),  # 🔒 n'exige un token qu'en AUTH_MODE=full
):
    societes = list_societes(limit=limit)

    for soc in societes:
        soc["secteur"] = soc.get("secteur", "inconnu")

    # ✅ Retourner directement une liste
    return societes
