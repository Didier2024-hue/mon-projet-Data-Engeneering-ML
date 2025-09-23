from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import io
import csv
import pandas as pd
from services.mongo_service import get_last_comments

router = APIRouter(prefix="/export", tags=["Export"])

# -----------------------
# GET /export  → pour tests unitaires
# -----------------------
@router.get("/")
async def export_data():
    """
    Endpoint factice pour les tests.
    Retourne un JSON simple confirmant que l'export est disponible.
    """
    return {"export": "ok", "format": "json"}

# -----------------------
# POST /export  → vrai endpoint d'export
# -----------------------
@router.post("/")
def export_comments_endpoint(data: dict):
    societe_id = data.get("societe_id")
    n_commentaires = data.get("n_commentaires", 50)
    formats = data.get("formats", ["csv"])

    if not societe_id:
        raise HTTPException(status_code=400, detail="societe_id requis pour l'export")

    # Récupérer les commentaires
    comments = get_last_comments(societe_id=societe_id, limit=n_commentaires)
    
    if not comments:
        raise HTTPException(status_code=404, detail="Aucun commentaire trouvé pour cette société")

    # Normaliser les données pour pandas
    df = pd.DataFrame(comments)
    df = df[["auteur", "commentaire", "note_commentaire", "date", "societe_nom"]]

    responses = {}

    if "csv" in formats:
        output_csv = io.StringIO()
        df.to_csv(output_csv, index=False)
        output_csv.seek(0)
        responses["csv"] = StreamingResponse(
            output_csv,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={societe_id}_comments.csv"}
        )

    if "xls" in formats or "xlsx" in formats:
        output_xls = io.BytesIO()
        df.to_excel(output_xls, index=False, engine="openpyxl")
        output_xls.seek(0)
        responses["xlsx"] = StreamingResponse(
            output_xls,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={societe_id}_comments.xlsx"}
        )

    if "json" in formats:
        responses["json"] = JSONResponse(content=df.to_dict(orient="records"))

    if not responses:
        raise HTTPException(status_code=400, detail="Format non supporté. Formats possibles: csv, xls, json")

    # Si un seul format demandé, retourner directement ce fichier
    if len(responses) == 1:
        return list(responses.values())[0]

    # Si plusieurs formats, retourner un dict avec tous les types disponibles
    return responses
