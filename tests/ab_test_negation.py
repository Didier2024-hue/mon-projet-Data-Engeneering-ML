# -*- coding: utf-8 -*-
import os
import glob
import re
import joblib
from dotenv import load_dotenv

# ----------------------------
# 1) Phrases de test
# ----------------------------
phrases = {
    "positif": [
        "Super service, je suis très satisfait !",
        "Livraison rapide et produit conforme",
        "Expérience excellente du début à la fin"
    ],
    "neutre": [
        "C'était correct, sans plus",
        "Pas de problème mais rien d'extraordinaire",
        "Service moyen, livraison standard"
    ],
    "negatif": [
        "Service catastrophique, à fuir",
        "Je ne suis pas content du tout",
        "Produit défectueux et aucune réponse du SAV"
    ]
}

# ----------------------------
# 2) Fonction de marquage de négation (même que dans ton script)
# ----------------------------
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

# ----------------------------
# 3) Chargement env + tfidf + modèles
# ----------------------------
def load_models_and_vectorizer():
    load_dotenv()  # charge le .env à la racine où tu exécutes le script
    data_model = os.getenv("DATA_MODEL")
    if not data_model or not os.path.isdir(data_model):
        raise RuntimeError("DATA_MODEL non défini ou invalide dans le .env")

    # Vectorizer
    tfidf_path = os.path.join(data_model, "tfidf_vectorizer_dual.pkl")
    if not os.path.isfile(tfidf_path):
        raise RuntimeError(f"Vectorizer introuvable à : {tfidf_path}")
    tfidf = joblib.load(tfidf_path)

    # Modèles
    models = {"note": {}, "sentiment": {}}
    pattern = re.compile(r"(?P<algo>.+)_(?P<task>sentiment|note)\.pkl$", re.IGNORECASE)
    for pkl in glob.glob(os.path.join(data_model, "*.pkl")):
        fname = os.path.basename(pkl)
        if fname == "tfidf_vectorizer_dual.pkl":
            continue
        m = pattern.match(fname)
        if not m:
            continue
        algo = m.group("algo").lower()
        task = m.group("task").lower()
        try:
            models[task][algo] = joblib.load(pkl)
        except Exception as e:
            print(f"[WARN] Impossible de charger {fname}: {e}")
    return tfidf, models

# ----------------------------
# 4) Prédictions A/B
# ----------------------------
def run_ab_test(tfidf, models):
    changes = []  # pour compter les différences entre sans/avec négation

    for task, algos in models.items():
        if not algos:
            continue
        print("\n" + "="*80)
        print(f"TÂCHE : {task.upper()}")
        print("="*80)

        for algo, model in algos.items():
            print(f"\n--- Modèle : {algo} ---")

            for cat, samples in phrases.items():
                print(f"\n>>> Catégorie : {cat}")
                for text in samples:
                    text_neg = mark_negation(text)

                    # Sans négation
                    X_raw = tfidf.transform([text])
                    pred_raw = model.predict(X_raw)[0]

                    # Avec négation
                    X_neg = tfidf.transform([text_neg])
                    pred_neg = model.predict(X_neg)[0]

                    diff = pred_raw != pred_neg
                    if diff:
                        changes.append((task, algo, text, pred_raw, pred_neg))

                    print(f"- Phrase : {text}")
                    print(f"    Sans négation -> {pred_raw}")
                    print(f"    Avec négation -> {pred_neg} {'(DIFF)' if diff else ''}")

    # Résumé
    print("\n" + "#"*80)
    print("RÉSUMÉ DES DIFFÉRENCES")
    print("#"*80)
    if not changes:
        print("Aucune différence de prédiction entre 'sans' et 'avec' négation sur ces 9 phrases.")
    else:
        print(f"{len(changes)} différences observées :")
        for (task, algo, text, pr, pn) in changes:
            print(f"[{task} | {algo}] '{text}' -> sans:{pr} | avec:{pn}")

if __name__ == "__main__":
    tfidf, models = load_models_and_vectorizer()
    run_ab_test(tfidf, models)

