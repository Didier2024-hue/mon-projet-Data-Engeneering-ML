import os
import re
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

# Chargement des variables d'environnement
load_dotenv()

DATA_PROCESSED = os.getenv("DATA_PROCESSED")
DATA_MODEL = os.getenv("DATA_MODEL")
DATA_REPORT = os.getenv("DATA_REPORT")  # <-- variable pour les reports PNG
os.makedirs(DATA_MODEL, exist_ok=True)
os.makedirs(DATA_REPORT, exist_ok=True)  # création du dossier report si nécessaire

# 1. Chargement des données
file_path = os.path.join(DATA_PROCESSED, "export_preprocess_clean_avis.csv")
print("\n📥 Chargement des données...")
df = pd.read_csv(file_path)
print("Colonnes du fichier:", df.columns.tolist())

# 2. Nettoyage
print("\n📥 Nettoyage...")
df = df.dropna(subset=['commentaire'])
df = df[df['commentaire'].str.strip().astype(bool)]

# 3. Fonction avancée pour gérer la négation avec une fenêtre de 3 mots
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

df['commentaire_preprocessed'] = df['commentaire'].apply(mark_negation)

X = df['commentaire_preprocessed']
y_notes = df['note_commentaire']

def map_sentiment(note):
    if note == 1:
        return 'negatif'
    elif note == 5:
        return 'positif'
    else:
        return 'neutre'

y_sentiment = y_notes.apply(map_sentiment)

# 4. TF-IDF avec bigrammes et vocabulaire augmenté
print("\n✍️ Vectorisation TF-IDF avec bigrammes...")
tfidf = TfidfVectorizer(max_features=3000, ngram_range=(1, 2))
X_vect = tfidf.fit_transform(X)
joblib.dump(tfidf, os.path.join(DATA_MODEL, "tfidf_vectorizer_dual.pkl"))

# 5. Split train/test stratifié
print("\n🔀 Split train/test stratifié...")
sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_index, test_index in sss.split(X_vect, y_sentiment):
    X_train, X_test = X_vect[train_index], X_vect[test_index]
    y_train_sent, y_test_sent = y_sentiment.iloc[train_index], y_sentiment.iloc[test_index]
    y_train_note, y_test_note = y_notes.iloc[train_index], y_notes.iloc[test_index]

# 6. Définition des modèles
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000, class_weight='balanced'),
    "LinearSVC": LinearSVC(class_weight='balanced'),
    "RandomForest": RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
}

# 7. Entraînement et évaluation
tasks = {
    "sentiment": (y_train_sent, y_test_sent, ['negatif', 'neutre', 'positif']),
    "note": (y_train_note, y_test_note, [1, 2, 3, 4, 5])
}

results = []

def plot_top_features(model, feature_names, task, model_name, n_features=20):
    """Fonction pour afficher les features les plus importantes"""
    try:
        if hasattr(model, 'coef_'):
            # Pour les modèles linéaires
            coef = model.coef_
            if coef.shape[0] == 1:  # Cas de classification binaire
                coef = coef.flatten()
                importance = coef
            else:  # Cas multiclasse
                importance = np.mean(np.abs(coef), axis=0)
        elif hasattr(model, 'feature_importances_'):
            # Pour Random Forest
            importance = model.feature_importances_
        else:
            print(f"⚠ Impossible d'extraire les features importantes pour {model_name}")
            return
        
        # Tri des features par importance
        indices = np.argsort(np.abs(importance))[-n_features:]
        top_words = feature_names[indices]
        top_values = importance[indices]
        
        # Création du graphique
        plt.figure(figsize=(10, 6))
        colors = ['green' if v > 0 else 'red' for v in top_values] if hasattr(model, 'coef_') else 'blue'
        plt.barh(top_words, top_values, color=colors)
        title = f"Top {n_features} mots influents - {model_name} ({task})"
        plt.title(title)
        plt.xlabel("Importance" if hasattr(model, 'feature_importances_') else "Valeur du coefficient")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        # Sauvegarde et affichage
        filename = f"report_preprocess_top{n_features}_{model_name.lower()}_{task}.png"
        plt.savefig(os.path.join(DATA_REPORT, filename))
        plt.close()
        print(f"✅ Top {n_features} mots sauvegardés dans : {filename}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des top features pour {model_name} ({task}): {str(e)}")

for task, (y_tr, y_te, labels) in tasks.items():
    print(f"\n===== Tâche : {task.upper()} =====")

    for name, model in models.items():
        print(f"\n🔧 Entraînement du modèle {name}...")
        model.fit(X_train, y_tr)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_te, y_pred)
        f1 = f1_score(y_te, y_pred, average='macro', zero_division=0)
        print(f"🎯 Accuracy : {acc * 100:.2f}% | 🧮 F1-score macro : {f1:.4f}")
        print(classification_report(y_te, y_pred, zero_division=0))

        # Matrice de confusion pour tous les modèles
        cm = confusion_matrix(y_te, y_pred, labels=labels)
        plt.figure(figsize=(6, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
        plt.title(f"Matrice de confusion - {name} ({task})")
        plt.xlabel("Prédit")
        plt.ylabel("Réel")
        plt.tight_layout()
        cm_filename = f"report_preprocess_confusion_{name.lower()}_{task}.png"
        plt.savefig(os.path.join(DATA_REPORT, cm_filename))
        plt.close()
        print(f"✅ Matrice de confusion sauvegardée : {cm_filename}")
        
        # Top features pour tous les modèles
        feature_names = np.array(tfidf.get_feature_names_out())
        plot_top_features(model, feature_names, task, name)

        path = os.path.join(DATA_MODEL, f"{name.lower()}_{task}.pkl")
        joblib.dump(model, path)
        print(f"✅ Modèle sauvegardé : {path}")

        results.append({
            "Tâche": task,
            "Modèle": name,
            "Accuracy": round(acc, 4),
            "F1_score_macro": round(f1, 4)
        })

# 8. Résumé comparatif
print("\n📊 Résultats comparatifs :")
df_results = pd.DataFrame(results)
print(df_results)

df_results.to_csv(os.path.join(DATA_PROCESSED, "resultats_modeles.csv"), index=False)
print("\n💾 Résultats sauvegardés dans : resultats_modeles.csv")

# 9. Tests manuels sur 9 phrases
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
        "Produit défectueux et aucune réponse du SAV",
        "Service client totalement inefficace et incapable de résoudre le moindre problème",
        "Produit arrivé endommagé après une livraison exceptionnellement longue",
        "Je ne recommanderai jamais cette entreprise à qui que ce soit",
        "Expérience désastreuse du début à la fin, aucune compensation offerte",
        "Le SAV est une véritable blague, impossible d'obtenir une réponse claire",
        "Qualité de fabrication médiocre pour un prix pourtant élevé",
        "Fausses descriptions sur le site, produit ne correspond pas du tout aux photos",
        "Processus de retour compliqué et volontairement dissuasif",
        "Facturation abusive avec des frais cachés non mentionnés initialement",
        "Application buggée qui plante constamment, rendant le service inutilisable"
    ]
}

print("\n===== Tests manuels sur 9 phrases =====")
for cat, samples in phrases.items():
    for phrase in samples:
        vec = tfidf.transform([mark_negation(phrase)])
        print(f"\n📝 Phrase ({cat}) : {phrase}")
        for task in ["sentiment", "note"]:
            print(f"🔎 Prédictions {task} :", end=" ")
            for name in models:
                model_path = os.path.join(DATA_MODEL, f"{name.lower()}_{task}.pkl")
                mdl = joblib.load(model_path)
                pred = mdl.predict(vec)[0]
                print(f"{name} = {pred}", end=" | ")
            print()

print("\n✔ Script complet terminé.")