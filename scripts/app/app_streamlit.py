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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)

# Récupération des variables d'environnement
DATA_MODEL = os.getenv("DATA_MODEL")
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

def list_available_models(models_dir: str):
    """ Retourne un dict {task: {algo: filename}} sans charger les modèles. """
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
        models[task][algo] = filename

    return models

@st.cache_resource
def load_single_model(model_path: str):
    """ Charge un seul modèle ML (optimisation mémoire). """
    return joblib.load(model_path)

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

available_models = list_available_models(DATA_MODEL)

# =========================
# UI
# =========================
st.title("🧪 Testeur d'avis – multi-modèles (note & sentiment)")

with st.sidebar:
    st.header("⚙️ Paramètres")

    # Liste des tâches
    available_tasks = [t for t, d in available_models.items() if len(d) > 0]
    if not available_tasks:
        st.error("Aucun modèle détecté dans le dossier.")
        st.stop()

    task = st.selectbox(
        "Tâche",
        available_tasks,
        format_func=lambda x: "Prédiction de la note (1-5)" if x == "note" else "Analyse de sentiment"
    )

    # On limite d'abord à "linear" uniquement
    show_all = st.checkbox("Activer les modèles avancés")

    if show_all:
        algos = list(available_models[task].keys())
    else:
        # On affiche seulement linear_svc si présent
        algos = [a for a in available_models[task].keys() if "linear" in a]
        if not algos:
            algos = list(available_models[task].keys())  # fallback, mais normalement inutile

    # Sélection du modèle avec linear par défaut
    default_algo_index = 0
    if "linear" in algos:
        default_algo_index = algos.index("linear")

    model_name = st.selectbox("Modèle", algos, index=default_algo_index)

    st.markdown("**Modèles trouvés :**")
    for t, algos_d in available_models.items():
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

    # Chargement du modèle sélectionné
    filename = available_models[task][model_name]
    model_path = os.path.join(DATA_MODEL, filename)
    model = load_single_model(model_path)

    # Traitement
    phrases = (
        [l.strip() for l in user_input.split("\n") if l.strip()]
        if batch_mode else
        [user_input.strip()]
    )

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

    # Affichage
    for r in results:
        st.write("---")
        st.write(f"**Texte :** {r['phrase']}")
        st.success(f"**Prédiction ({task}) :** {r['prediction']}")
        if "sentiment_from_note" in r:
            st.info(f"Sentiment approximatif dérivé de la note : **{r['sentiment_from_note']}**")
        if r.get("proba"):
            st.write("Probabilités :")
            st.json(r["proba"])
