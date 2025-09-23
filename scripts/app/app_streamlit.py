# -*- coding: utf-8 -*-
# streamlit run app_streamlit.py

import os
import re
import glob
import joblib
import numpy as np
import streamlit as st
from sklearn.base import ClassifierMixin
from dotenv import load_dotenv

# =========================
# Chargement du .env
# =========================
from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables du .env dans os.environ

model_dir = os.getenv("DATA_MODEL")

if model_dir is None:
    raise ValueError("Le dossier des modèles 'DATA_MODEL' n'est pas défini dans .env ou n'a pas été chargé")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")  # On remonte d'un dossier si besoin
load_dotenv(ENV_PATH)

# Récupération des variables d'environnement
DATA_MODEL = os.getenv("DATA_MODEL")  # Chemin vers les modèles
if DATA_MODEL is None or not os.path.isdir(DATA_MODEL):
    st.error(f"Le dossier des modèles '{DATA_MODEL}' n'existe pas ou n'est pas défini.")
    st.stop()

TFIDF_NAME = "tfidf_vectorizer_dual.pkl"

# =========================
# Utils
# =========================
@st.cache_resource
def load_tfidf(path: str):
    return joblib.load(path)

@st.cache_resource
def load_all_models(models_dir: str):
    models = {"note": {}, "sentiment": {}}
    pattern = re.compile(r"(?P<algo>.+)_(?P<task>sentiment|note)\.pkl$", re.IGNORECASE)

    for pkl_path in glob.glob(os.path.join(models_dir, "*.pkl")):
        filename = os.path.basename(pkl_path)
        if filename == TFIDF_NAME:
            continue
        m = pattern.match(filename)
        if not m:
            continue
        algo = m.group("algo").lower()
        task = m.group("task").lower()
        try:
            model = joblib.load(pkl_path)
            models[task][algo] = model
        except Exception as e:
            st.warning(f"Impossible de charger {filename} : {e}")
    return models

def mark_negation(text, window=3):
    negation_words = {"ne", "pas", "plus", "jamais", "rien", "aucun", "sans", "nul"}
    punctuation = {".", ",", ";", ":", "!", "?"}
    stop_words = {"mais", "et", "ou", "donc", "or", "ni", "car"}

    tokens = text.split()
    new_tokens = []
    neg_countdown = 0

    for tok in tokens:
        tok_lower = tok.lower()
        if tok_lower in negation_words:
            neg_countdown = window
            new_tokens.append(tok)
        elif neg_countdown > 0:
            if tok_lower in punctuation or tok_lower in stop_words:
                neg_countdown = 0
                new_tokens.append(tok)
            else:
                new_tokens.append("NOT_" + tok)
                neg_countdown -= 1
        else:
            new_tokens.append(tok)
    return " ".join(new_tokens)

def map_sentiment_from_note(note: int):
    return "negatif" if note == 1 else "positif" if note == 5 else "neutre"

def predict_with_optional_proba(model: ClassifierMixin, X):
    y_pred = model.predict(X)
    proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba_values = model.predict_proba(X)[0]
            classes = model.classes_
            proba = {str(c): float(p) for c, p in zip(classes, proba_values)}
        except Exception:
            pass
    return y_pred[0], proba

# =========================
# Chargements
# =========================
tfidf_path = os.path.join(DATA_MODEL, TFIDF_NAME)
tfidf = load_tfidf(tfidf_path)
models = load_all_models(DATA_MODEL)

# =========================
# UI
# =========================
st.title("🧪 Testeur d'avis – multi-modèles (note & sentiment)")

with st.sidebar:
    st.header("⚙️ Paramètres")
    available_tasks = [t for t, d in models.items() if len(d) > 0]
    if not available_tasks:
        st.error("Aucun modèle détecté dans le dossier.")
        st.stop()
    task = st.selectbox("Tâche", available_tasks, format_func=lambda x: "Prédiction de la note (1-5)" if x == "note" else "Analyse de sentiment")
    algos = list(models[task].keys())
    model_name = st.selectbox("Modèle", algos)
    st.markdown("**Modèles trouvés :**")
    for t, algos_d in models.items():
        if algos_d:
            st.write(f"- **{t}** :", ", ".join(sorted(algos_d.keys())))

user_input = st.text_area("✍️ Entrez un commentaire à évaluer :", height=150)
col1, col2 = st.columns(2)
with col1:
    do_predict = st.button("Prédire")
with col2:
    batch_mode = st.toggle("Mode batch (1 phrase par ligne)")

if do_predict:
    if not user_input.strip():
        st.warning("Veuillez entrer un commentaire valide.")
        st.stop()
    model = models[task][model_name]
    phrases = [l.strip() for l in user_input.split("\n") if l.strip()] if batch_mode else [user_input.strip()]
    results = []
    for phrase in phrases:
        phrase_proc = mark_negation(phrase)
        X_vec = tfidf.transform([phrase_proc])
        pred, proba = predict_with_optional_proba(model, X_vec)
        out = {"phrase": phrase, "prediction": pred}
        if task == "note":
            try:
                out["sentiment_from_note"] = map_sentiment_from_note(int(pred))
            except Exception:
                pass
        if proba:
            out["proba"] = proba
        results.append(out)
    for r in results:
        st.write("---")
        st.write(f"**Texte :** {r['phrase']}")
        st.success(f"**Prédiction ({task}) :** {r['prediction']}")
        if "sentiment_from_note" in r:
            st.info(f"Sentiment approximatif dérivé de la note : **{r['sentiment_from_note']}**")
        if r.get("proba"):
            st.write("Probabilités :")
            st.json(r["proba"])
