import os
import nltk

# Définir manuellement le chemin des ressources sur sda2
BASE_PATH = "/home/datascientest/cde/data/processed/resources"
NLTK_PATH = os.path.join(BASE_PATH, "nltk_data")

# Définir les variables d’environnement avant toute utilisation
os.environ['NLTK_DATA'] = NLTK_PATH

# Ajouter ce chemin aux chemins de recherche de nltk
nltk.data.path.append(NLTK_PATH)

# Télécharger les stopwords dans ce dossier
nltk.download("stopwords", download_dir=NLTK_PATH)

print(f"✅ Stopwords téléchargés dans : {NLTK_PATH}")

