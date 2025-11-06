import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 📥 1. Chargement
print("📥 Chargement des données...")
file_path = "/home/datascientest/cde/data/processed/preprocessed_clean_avis_avec_sentiments.csv"
df = pd.read_csv(file_path)
print(f"✅ Données chargées : {df.shape[0]} lignes")

# 🧹 2. Nettoyage
df = df.dropna(subset=['commentaire_preprocessed'])
df = df[df['commentaire_preprocessed'].str.strip().astype(bool)]
print(f"✅ Commentaires valides : {df.shape[0]}")

# 🧠 3. Gestion de la négation
def preserve_negation(text):
    return text.replace("pas ", "pas_").replace("non ", "non_")

df['commentaire_preprocessed'] = df['commentaire_preprocessed'].apply(preserve_negation)

# 🏷️ 4. Regroupement des classes en 3 catégories
def simplifier_note(n):
    if n == 1:
        return 'negatif'
    elif n == 5:
        return 'positif'
    else:
        return 'neutre'

X = df['commentaire_preprocessed']
y = df['note_commentaire'].apply(simplifier_note)
print(f"🔢 Répartition des classes :\n{y.value_counts()}")

# ✍️ 5. Vectorisation TF-IDF
print("✍️ TF-IDF...")
tfidf = TfidfVectorizer(max_features=1000)
X_vect = tfidf.fit_transform(X)
joblib.dump(tfidf, "/home/datascientest/cde/data/model/tfidf_vectorizer_3classes.pkl")

# 🔀 6. Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X_vect, y, test_size=0.2, random_state=42, stratify=y
)
print(f"📚 Train : {X_train.shape[0]} | 🧪 Test : {X_test.shape[0]}")

# 🤖 7. Modèles à tester
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000, class_weight='balanced'),
    "LinearSVC": LinearSVC(class_weight='balanced')
}

results = {}

for name, model in models.items():
    print(f"\n🔧 Entraînement du modèle : {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"🎯 Accuracy ({name}) : {acc * 100:.2f}%")
    print("\n📝 Rapport de classification :\n")
    print(classification_report(y_test, y_pred))
    
    # 📉 Matrice de confusion
    cm = confusion_matrix(y_test, y_pred, labels=['negatif', 'neutre', 'positif'])
    plt.figure(figsize=(7, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['negatif', 'neutre', 'positif'],
                yticklabels=['negatif', 'neutre', 'positif'])
    plt.title(f"Matrice de Confusion - {name}")
    plt.xlabel("Prédit")
    plt.ylabel("Réel")
    plt.tight_layout()
    plt.show()
    
    # Sauvegarde du modèle
    model_path = f"/home/datascientest/cde/data/model/{name.lower()}_3classes.pkl"
    joblib.dump(model, model_path)
    print(f"✅ Modèle {name} sauvegardé dans {model_path}")
    
    results[name] = acc

# ✅ Résumé final
print("\n📊 Résumé des performances :")
for name, acc in results.items():
    print(f" - {name} : {acc * 100:.2f}%")

print("\n✔ Script terminé.")

