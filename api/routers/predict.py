from fastapi import APIRouter, HTTPException, Depends
from routers.auth import guard, PublicUser 
from pydantic import BaseModel
from pathlib import Path
import joblib
import os
import logging
from dotenv import load_dotenv

# Charger .env.api
load_dotenv("/home/datascientest/cde/api/.env.api")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/predict", tags=["Prédictions"])

# Chemins depuis .env
MODEL_PATH = Path(os.getenv("DATA_MODEL", "/home/datascientest/cde/data/model"))

def safe_load(path: Path):
    try:
        return joblib.load(path)
    except Exception as e:
        logger.warning(f"Impossible de charger {path.name}: {e}")
        return None

tfidf = safe_load(MODEL_PATH / "tfidf_vectorizer_dual.pkl")
model_note = safe_load(MODEL_PATH / "linearsvc_note.pkl")
model_sentiment = safe_load(MODEL_PATH / "linearsvc_sentiment.pkl")

if tfidf is None:
    logger.warning("TFIDF vectorizer non chargé")
if model_note is None:
    logger.warning("Modèle note non chargé")
if model_sentiment is None:
    logger.warning("Modèle sentiment non chargé")

# ✅ Seulement "commentaire"
class PredictRequest(BaseModel):
    commentaire: str

def preprocess_text(text: str) -> str:
    return text.lower().strip()

# -----------------------
# Endpoint /predict/note
# -----------------------
@router.post("/note")
def predict_note(req: PredictRequest, user: PublicUser | None = Depends(guard("sensitive"))):
    if tfidf is None or model_note is None:
        raise HTTPException(status_code=503, detail="Modèle ou vectorizer pour 'note' non disponible")

    X = tfidf.transform([preprocess_text(req.commentaire)])
    try:
        pred = model_note.predict(X)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur prediction note: {e}")

    return {"commentaire": req.commentaire, "note": int(pred)}

# -----------------------
# Endpoint /predict/sentiment
# -----------------------
@router.post("/sentiment")
def predict_sentiment(req: PredictRequest, user: PublicUser | None = Depends(guard("sensitive"))):
    if tfidf is None or model_sentiment is None:
        raise HTTPException(status_code=503, detail="Modèle ou vectorizer pour 'sentiment' non disponible")

    X = tfidf.transform([preprocess_text(req.commentaire)])
    try:
        pred = model_sentiment.predict(X)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur prediction sentiment: {e}")

    sentiment_label = "positif" if str(pred) == "1" else "négatif"
    return {"commentaire": req.commentaire, "sentiment": sentiment_label}
