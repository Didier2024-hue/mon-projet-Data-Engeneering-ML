import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE

# 📥 Étape 1 : Chargement des données
print("📥 Chargement des données...")
file_path = "/home/datascientest/cde/data/processed/preprocessed_clean_avis_avec_sentiments.csv"
df = pd.read_csv(file_path)
print(f"✅ Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")

# Étape 2 : Nettoyage des commentaires invalides
print("Nettoyage des commentaires vides ou NaN...")
df = df.dropna(subset=['commentaire_preprocessed'])
df = df[df['commentaire_preprocessed'].str.strip().astype(bool)]
print(f"✅ Commentaires valides : {df.shape[0]}")

# Étape 3 : Préparation des variables
X = df['commentaire_preprocessed']
y = df['note_commentaire']

# ✍️ Étape 4 : Vectorisation TF-IDF
print("✍️ Vectorisation TF-IDF...")
tfidf = TfidfVectorizer(max_features=1000)
X_vect = tfidf.fit_transform(X)
joblib.dump(tfidf, "/home/datascientest/cde/data/model/tfidf_vectorizer.pkl")
print(f"✅ TF-IDF terminé : {X_vect.shape[0]} documents, {X_vect.shape[1]} dimensions")

# Étape 5 : Top 20 mots TF-IDF
word_scores = np.asarray(X_vect.sum(axis=0)).ravel()
vocab = tfidf.get_feature_names_out()
top_idx = word_scores.argsort()[-20:][::-1]
top_words = [vocab[i] for i in top_idx]
top_scores = [word_scores[i] for i in top_idx]

plt.figure(figsize=(10, 6))
plt.barh(top_words[::-1], top_scores[::-1], color=plt.cm.viridis(np.linspace(0, 1, len(top_words))))
plt.xlabel("Score TF-IDF cumulé")
plt.title("Top 20 mots les plus fréquents")
plt.tight_layout()
plt.savefig("/home/datascientest/cde/data/processed/tfidf_top_words.png")
plt.close()

# ⚖️ Étape 6 : Équilibrage avec SMOTE
print("⚖️ Application de SMOTE pour équilibrage des classes...")
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_vect, y)
print(f"✅ Données équilibrées : {X_resampled.shape[0]} échantillons")

# Étape 7 : PCA avant/après SMOTE
pca = PCA(n_components=2, random_state=42)
X_pca_before = pca.fit_transform(X_vect.toarray())
X_pca_after = pca.fit_transform(X_resampled.toarray())

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].scatter(X_pca_before[:, 0], X_pca_before[:, 1], c=y, cmap='tab10', s=10)
axes[0].set_title("Avant SMOTE")
axes[1].scatter(X_pca_after[:, 0], X_pca_after[:, 1], c=y_resampled, cmap='tab10', s=10)
axes[1].set_title("Après SMOTE")
plt.savefig("/home/datascientest/cde/data/processed/smote_projection_pca.png")
plt.close()

# 🔀 Étape 8 : Split train/test
print("🔀 Split des données (80% train / 20% test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X_resampled, y_resampled, test_size=0.2, random_state=42, stratify=y_resampled
)
print(f"📚 Train : {X_train.shape[0]} | 🧪 Test : {X_test.shape[0]}")

# 🌲 Étape 9 : GridSearch pour optimiser Random Forest
print("🌲 Recherche des meilleurs hyperparamètres Random Forest...")
param_grid = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5]
}
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=3,
    n_jobs=-1,
    scoring='accuracy',
    verbose=1
)
grid_search.fit(X_train, y_train)
best_rf = grid_search.best_estimator_
print(f"✅ Meilleur modèle : {grid_search.best_params_}")

# 📈 Étape 10 : Évaluation
print("📈 Évaluation du modèle sélectionné...")
y_pred = best_rf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"🎯 Accuracy : {accuracy:.4f}")
print("\n📝 Rapport de classification :\n")
print(classification_report(y_test, y_pred))

# Étape 11 : Matrice de confusion
print("📉 Matrice de confusion...")
cm = confusion_matrix(y_test, y_pred, labels=sorted(y.unique()))
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=sorted(y.unique()), yticklabels=sorted(y.unique()))
plt.xlabel("Prédit")
plt.ylabel("Réel")
plt.title("Matrice de Confusion")
plt.tight_layout()
plt.savefig("/home/datascientest/cde/data/processed/matrice_de_confusion.png")
plt.close()

# 💾 Étape 12 : Sauvegarde du meilleur modèle
print("💾 Sauvegarde du modèle optimisé...")
model_dir = "/home/datascientest/cde/data/model"
os.makedirs(model_dir, exist_ok=True)
joblib.dump(best_rf, os.path.join(model_dir, "random_forest_model.pkl"))
print("✅ Modèle sauvegardé")

print("\n✔ Script terminé avec succès.")
