import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# 📥 1. Chargement des données
print("📥 Chargement des données...")
file_path = "/home/datascientest/cde/data/processed/preprocessed_clean_avis_avec_sentiments.csv"
df = pd.read_csv(file_path)
print(f"✅ Données chargées : {df.shape[0]} lignes")

# 🧹 2. Nettoyage
df = df.dropna(subset=['commentaire_preprocessed'])
df = df[df['commentaire_preprocessed'].str.strip().astype(bool)]
print(f"✅ Commentaires valides : {df.shape[0]}")

# 🧠 3. Gestion simple de la négation
def preserve_negation(text):
    return text.replace("pas ", "pas_").replace("non ", "non_")

df['commentaire_preprocessed'] = df['commentaire_preprocessed'].apply(preserve_negation)

X = df['commentaire_preprocessed']
y = df['note_commentaire']

# ✍️ 4. TF-IDF
print("✍️ Vectorisation TF-IDF...")
tfidf = TfidfVectorizer(max_features=1000)
X_vect = tfidf.fit_transform(X)
joblib.dump(tfidf, "/home/datascientest/cde/data/model/tfidf_vectorizer.pkl")
print(f"✅ TF-IDF : {X_vect.shape}")

# 🔀 5. Split
print("🔀 Split train/test...")
X_train, X_test, y_train, y_test = train_test_split(
    X_vect, y, test_size=0.2, random_state=42, stratify=y
)
print(f"📚 Train : {X_train.shape[0]} | 🧪 Test : {X_test.shape[0]}")

# 🌿 6. GridSearch Logistic Regression
print("🌿 Optimisation du modèle Logistic Regression...")
param_grid = {
    "C": [0.01, 0.1, 1, 10]
}
grid_search = GridSearchCV(
    LogisticRegression(max_iter=1000, class_weight='balanced'),
    param_grid,
    scoring='f1_weighted',
    cv=3,
    verbose=1,
    n_jobs=-1
)
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_
print(f"✅ Meilleur modèle : {grid_search.best_params_}")

# 📈 7. Évaluation
print("📈 Évaluation...")
y_pred = best_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"🎯 Accuracy : {accuracy * 100:.2f}%")
print("\n📝 Rapport de classification :\n")
print(classification_report(y_test, y_pred))

# 📉 8. Matrice de confusion (affichage + sauvegarde)
print("📉 Matrice de confusion...")
cm = confusion_matrix(y_test, y_pred, labels=sorted(y.unique()))
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=sorted(y.unique()), yticklabels=sorted(y.unique()))
plt.xlabel("Prédit")
plt.ylabel("Réel")
plt.title("Matrice de Confusion")
plt.tight_layout()
plt.show()  # 👈 Affichage à l’écran
plt.savefig("/home/datascientest/cde/data/processed/matrice_confusion_logreg.png")
plt.close()

# 💾 9. Sauvegarde
print("💾 Sauvegarde du modèle...")
model_dir = "/home/datascientest/cde/data/model"
os.makedirs(model_dir, exist_ok=True)
joblib.dump(best_model, os.path.join(model_dir, "logistic_model.pkl"))
print("✅ Modèle sauvegardé")

print("\n✔ Script terminé avec succès.")

