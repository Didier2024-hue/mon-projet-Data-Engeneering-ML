from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, model_validator
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

# ✅ Accepte "text" OU "commentaire", mais au moins un obligatoire
class TextRequest(BaseModel):
    text: str | None = None
    commentaire: str | None = None

    @model_validator(mode="after")
    def check_at_least_one(cls, values):
        if not values.text and not values.commentaire:
            raise ValueError("Champ 'text' ou 'commentaire' requis")
        return values

    def get_text(self) -> str:
        return self.text or self.commentaire

def preprocess_text(text: str) -> str:
    return text.lower().strip()

# -----------------------
# Endpoint principal /predict
# -----------------------
@router.post("/")
def predict_commentaire(req: TextRequest):
    if tfidf is None:
        return {"prediction": "indisponible"}

    X = tfidf.transform([preprocess_text(req.get_text())])

    # Sentiment prioritaire
    if model_sentiment:
        try:
            pred = model_sentiment.predict(X)[0]
            sentiment_label = "positif" if str(pred) == "1" else "négatif"
            return {"prediction": sentiment_label}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur prediction sentiment: {e}")

    # Sinon fallback sur la note
    if model_note:
        try:
            pred = model_note.predict(X)[0]
            return {"prediction": int(pred)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur prediction note: {e}")

    return {"prediction": "indisponible"}

# -----------------------
# Endpoint /predict/note
# -----------------------
@router.post("/note")
def predict_note(req: TextRequest):
    if tfidf is None or model_note is None:
        raise HTTPException(status_code=503, detail="Modèle ou vectorizer pour 'note' non disponible")

    X = tfidf.transform([preprocess_text(req.get_text())])
    try:
        pred = model_note.predict(X)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur prediction note: {e}")

    try:
        return {"note": int(pred)}
    except Exception:
        return {"note": pred}

# -----------------------
# Endpoint /predict/sentiment
# -----------------------
@router.post("/sentiment")
def predict_sentiment(req: TextRequest):
    if tfidf is None or model_sentiment is None:
        raise HTTPException(status_code=503, detail="Modèle ou vectorizer pour 'sentiment' non disponible")

    X = tfidf.transform([preprocess_text(req.get_text())])
    try:
        pred = model_sentiment.predict(X)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur prediction sentiment: {e}")

    sentiment_label = "positif" if str(pred) == "1" else "négatif"
    return {"sentiment": sentiment_label}
