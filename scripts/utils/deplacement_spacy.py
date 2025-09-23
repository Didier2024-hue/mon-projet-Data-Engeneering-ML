import os
import nltk
from spacy.cli import download

# Définir la base de stockage sur sda2
BASE_PATH = "/home/datascientest/cde/data/processed/resources"
NLTK_PATH = os.path.join(BASE_PATH, "nltk_data")
XDG_CACHE_PATH = os.path.join(BASE_PATH, "xdg_cache")

# 🔧 Variables d’environnement
os.environ["NLTK_DATA"] = NLTK_PATH
os.environ["XDG_CACHE_HOME"] = XDG_CACHE_PATH  # spaCy utilise ce cache

# 📚 Télécharger les stopwords dans sda2
nltk.data.path.append(NLTK_PATH)
nltk.download("stopwords", download_dir=NLTK_PATH)

# 📥 Télécharger le modèle spaCy (il sera mis dans ~/.cache/spacy par défaut)
download("fr_core_news_sm")

print("✅ Modèle spaCy téléchargé. Tu peux maintenant déplacer ~/.cache si tu veux tout centraliser.")

