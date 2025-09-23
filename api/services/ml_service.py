# mlservice.py
import os
import joblib
import glob
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

MODEL_DIR = os.getenv("DATA_MODEL", "/home/datascientest/cde/data/model")
TFIDF_NAME = "tfidf_vectorizer_dual.pkl"

def load_if_exists(path: str):
    try:
        return joblib.load(path)
    except Exception:
        return None

tfidf = load_if_exists(os.path.join(MODEL_DIR, TFIDF_NAME))

models: Dict[str, Dict[str, Optional[object]]] = {"note": {}, "sentiment": {}}
pattern = glob.glob(os.path.join(MODEL_DIR, "*.pkl"))
for path in pattern:
    fname = os.path.basename(path).lower()
    if "tfidf" in fname:
        continue
    if "note" in fname:
        models["note"]["linearsvc"] = load_if_exists(path)
    elif "sentiment" in fname:
        models["sentiment"]["linearsvc"] = load_if_exists(path)

def predict_text(text: str, task: str = "sentiment"):
    if tfidf is None or models.get(task, {}).get("linearsvc") is None:
        return {"error": "model or tfidf missing"}
    X_vec = tfidf.transform([text])
    model = models[task]["linearsvc"]
    y_pred = model.predict(X_vec)[0]
    proba = None
    if hasattr(model, "predict_proba"):
        proba_values = model.predict_proba(X_vec)[0]
        classes = model.classes_
        proba = {str(c): float(p) for c, p in zip(classes, proba_values)}
    return {"prediction": y_pred, "proba": proba}
