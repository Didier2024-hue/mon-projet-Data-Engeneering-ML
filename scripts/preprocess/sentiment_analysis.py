import os
import pandas as pd
import torch
from transformers import pipeline
from tqdm import tqdm
import warnings
import logging
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from dotenv import load_dotenv
from datetime import datetime
import matplotlib.pyplot as plt

# 🔧 Chargement des variables d'environnement
load_dotenv()
DATA_EXPORTS = os.getenv("DATA_EXPORTS")
DATA_PROCESSED = os.getenv("DATA_PROCESSED")
DATA_REPORT = os.getenv("DATA_REPORT")  # nouveau pour le dossier report
LOG_DIR = os.getenv("LOG_DIR")

# 📁 Fichiers d'entrée et sortie
INPUT_FILE = os.path.join(DATA_EXPORTS, "mongo_trustpilot_avis_trustpilot.csv")
OUTPUT_FILE = os.path.join(DATA_PROCESSED, "export_sentiment_analysis.csv")
STATS_FILE = os.path.join(DATA_PROCESSED, "stats_sentiment_analysis.csv")
REPORT_PNG = os.path.join(DATA_REPORT, "report_sentiment_analysis.png")

# 📚 Log automatique dans le bon répertoire
log_filename = os.path.join(LOG_DIR, f"bert_sentiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')

# Création des dossiers si absents
os.makedirs(DATA_PROCESSED, exist_ok=True)
os.makedirs(DATA_REPORT, exist_ok=True)

# 🔄 Renforcement des négations
def reinforce_negations(text):
    if pd.isna(text) or not isinstance(text, str):
        return text
    negations = ['pas', 'plus', 'jamais', 'rien', 'aucun', 'ni', 'nulle part', 'ne', 'non']
    tokens = text.split()
    result = []
    i = 0
    while i < len(tokens):
        word = tokens[i].lower()
        if word in negations:
            result.append('[NEG]')
            result.append(tokens[i])
            j = 1
            while j <= 3 and (i + j) < len(tokens):
                result.append(tokens[i + j])
                j += 1
            result.append('[/NEG]')
            i += j
        else:
            result.append(tokens[i])
            i += 1
    return ' '.join(result)

# 🤖 Analyseur BERT
class SentimentAnalyzer:
    def __init__(self):
        self.device = -1  # CPU
        self.model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
        self.batch_size = 4
        self.max_length = 128
        logger.info("🤖 Chargement du modèle BERT pour l'analyse de sentiment...")
        try:
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=self.device,
                truncation=True
            )
            logger.info("✅ Modèle BERT chargé avec succès !")
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du modèle : {str(e)}")
            raise

    def analyze_sentiment(self, text):
        try:
            if not text or pd.isna(text):
                return None, None
            result = self.pipeline(text[:self.max_length])
            return result[0]['label'], result[0]['score']
        except Exception as e:
            logger.warning(f"⚠️ Erreur sur le texte : {text[:50]}... - {str(e)}")
            return None, None

    def analyze_batch(self, texts):
        with ThreadPoolExecutor() as executor:
            results = list(tqdm(
                executor.map(self.analyze_sentiment, texts),
                total=len(texts),
                desc="🧠 Analyse des sentiments"
            ))
        return results

    def map_label_to_score(self, label):
        mapping = {
            '1 star': 1,
            '2 stars': 2,
            '3 stars': 3,
            '4 stars': 4,
            '5 stars': 5
        }
        return mapping.get(label, None)

# 📥 Chargement des données
def load_data(filepath):
    logger.info(f"📂 Chargement des données depuis {filepath}...")
    try:
        df = pd.read_csv(filepath)
        logger.info(f"✅ Données chargées : {len(df)} avis.")
        return df
    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement : {str(e)}")
        raise

# 🧹 Prétraitement
def preprocess_data(df):
    logger.info("🧹 Prétraitement des données...")
    df = df.drop_duplicates(subset=['commentaire'])
    df['commentaire'] = df['commentaire'].str.strip()
    df['commentaire'] = df['commentaire'].replace('', np.nan)
    df = df[df['commentaire'].notna()]
    logger.info("🔄 Renforcement des négations...")
    df['commentaire'] = df['commentaire'].apply(reinforce_negations)
    logger.info(f"📊 {len(df)} avis après nettoyage.")
    return df

# 📊 Génération du graphique de distribution
def plot_sentiment_distribution(stats_df):
    plt.figure(figsize=(8, 5))
    bars = plt.bar(stats_df["sentiment_note"], stats_df["count"], color='skyblue', edgecolor='black')
    plt.title("Répartition des avis par note de sentiment (1 à 5)", fontsize=14)
    plt.xlabel("Note de sentiment (1 = très négatif, 5 = très positif)")
    plt.ylabel("Nombre d'avis")
    plt.xticks(stats_df["sentiment_note"])

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + max(stats_df["count"]) * 0.01, f"{yval}", ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig(REPORT_PNG)
    logger.info(f"📈 Graphique sauvegardé dans {REPORT_PNG}")
    plt.close()

# 🚀 Programme principal
def main():
    try:
        df = load_data(INPUT_FILE)
        df = preprocess_data(df)

        analyzer = SentimentAnalyzer()
        texts = df['commentaire'].tolist()
        results = analyzer.analyze_batch(texts)

        labels, scores = zip(*results)
        df['sentiment_label'] = labels
        df['sentiment_score'] = scores
        df['sentiment_note'] = df['sentiment_label'].apply(analyzer.map_label_to_score)

        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        logger.info(f"💾 Résultats sauvegardés dans {OUTPUT_FILE}")
        print(f"\n💾 Fichier final : {OUTPUT_FILE} avec {len(df)} lignes")

        stats = df['sentiment_note'].value_counts().sort_index()
        logger.info("📈 Statistiques des notes de sentiment :")
        logger.info(stats)

        stats_df = stats.reset_index()
        stats_df.columns = ['sentiment_note', 'count']
        stats_df.to_csv(STATS_FILE, index=False, encoding='utf-8-sig')
        logger.info(f"📊 Statistiques sauvegardées dans {STATS_FILE}")
        print("\n📊 Répartition des sentiments :")
        print(stats_df.to_string(index=False))

        # Génération du PNG
        plot_sentiment_distribution(stats_df)

    except Exception as e:
        logger.error(f"❌ Erreur dans le processus principal : {str(e)}")

if __name__ == "__main__":
    main()
