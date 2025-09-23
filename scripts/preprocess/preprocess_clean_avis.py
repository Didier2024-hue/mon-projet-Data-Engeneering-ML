#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import string
import pandas as pd
from collections import Counter
from dotenv import load_dotenv

import nltk
from nltk.corpus import stopwords
import spacy
from gensim import corpora, models
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# =======================
# Chargement .env
# =======================
load_dotenv()
BASE_DIR = os.getenv("BASE_DIR")
if not BASE_DIR:
    print("❌ ERREUR : BASE_DIR non défini dans .env")
    exit(1)

DATA_PROCESSED = os.getenv("DATA_PROCESSED", f"{BASE_DIR}/data/processed")
DATA_REPORT = os.getenv("DATA_REPORT", f"{BASE_DIR}/data/report")

# Entrée / Sorties
INPUT_CSV = os.path.join(DATA_PROCESSED, "export_clean_data.csv")
OUTPUT_CSV = os.path.join(DATA_PROCESSED, "export_preprocess_clean_avis.csv")
OUTPUT_STATS = os.path.join(DATA_PROCESSED, "stats_preprocess_clean_avis.csv")
OUTPUT_WORDCLOUD = os.path.join(DATA_REPORT, "report_preprocess_clean_avis_word_cloud.png")
OUTPUT_SENTIMENT_HIST = os.path.join(DATA_REPORT, "report_preprocess_clean_avis_sentiment_hist.png")
OUTPUT_LDA_IMG = os.path.join(DATA_REPORT, "report_preprocess_clean_avis_lda.png")

os.makedirs(DATA_PROCESSED, exist_ok=True)
os.makedirs(DATA_REPORT, exist_ok=True)

# =======================
# Stopwords & spaCy
# =======================
nltk.download('stopwords', quiet=True)
stop_fr = set(stopwords.words('french'))
stop_en = set(stopwords.words('english'))

# ⚠️ Mots a bannir
CUSTOM_STOPWORDS = {
    'vinted', 'temu', 'chronopost', 'tesla', 'amazon', 'ubér', 'uber', 'ubereats',
    'être', 'avoir', 'faire', 'aller', 'venir', 'très', 'jai', 'cest', 'cette',
    'ce', 'ces', 'tout', 'tous', 'toute', 'toutes', 'comme', 'alors', 'alor', 'alorsque',
    'du', 'du coup', 'donc', 'car', 'parce', 'parce que', 'puis', 'ensuite', 'après',
    'un', 'une', 'des', 'le', 'la', 'les', 'au', 'aux', 'de', 'du', "d'",
    'mon', 'ton', 'son', 'ma', 'ta', 'sa', 'mes', 'tes', 'ses',
    'leur', 'leurs', 'notre', 'votre', 'nos', 'vos',
    'en', 'y', 'avec', 'sans', 'plus', 'sur', 'dire',
    'je', 'tu', 'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles',
    'ce', 'cet', 'cette', 'ces', 'tout', 'tous', 'toute', 'toutes',
    'comme', 'alors', 'alor', 'alorsque', 'du', 'du coup', 'donc',
    'car', 'parce', 'parce que', 'puis', 'ensuite', 'après',
    'un', 'une', 'des', 'le', 'la', 'les', 'au', 'aux', 'de', 'du', "d'",
    'mon', 'ton', 'son', 'ma', 'ta', 'sa', 'mes', 'tes', 'ses',
    'leur', 'leurs', 'notre', 'votre', 'nos', 'vos',
    'en', 'y', 'avec', 'sans', 'plus', 'sur', 'sous', 'dans', 'chez', 'etc'
}

try:
    nlp = spacy.load("fr_core_news_sm")
    print("✅ spaCy chargé avec le modèle français 'fr_core_news_sm'")
except Exception as e:
    print("❌ spaCy non chargé :", e)
    exit(1)

all_stopwords = stop_fr.union(stop_en).union(CUSTOM_STOPWORDS)

# Stopwords spécifiques au wordcloud
WC_STOPWORDS = set(STOPWORDS)
WC_STOPWORDS |= CUSTOM_STOPWORDS
WC_STOPWORDS.update(["neg", "cest", "cette", "ce", "ces", "tout", "tous", "toute", "toutes",
                    "comme", "alors", "alor", "alorsque", "du", "du coup", "donc",
                    "car", "parce", "parce que", "puis", "ensuite", "après",
                    "un", "une", "des", "le", "la", "les", "au", "aux", "de", "du", "d'",
                    "mon", "ton", "son", "ma", "ta", "sa", "mes", "tes", "ses",
                    "leur", "leurs", "notre", "votre", "nos", "vos",
                    "en", "y", "avec", "sans", "plus", "sur", "sous", "dans", "chez", "etc"])

# =======================
# Prétraitement + négation
# =======================
def preprocess_text_with_negation(text):
    if not isinstance(text, str):
        return ""

    # Nettoyage de base + retrait des balises [NEG]
    text = text.lower()
    text = re.sub(r"\[/?neg\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()

    doc = nlp(text)

    tokens = []
    negation_words = {"ne", "pas", "plus", "jamais", "rien", "personne", "aucun", "ni", "non"}  # <-- ajout de 'non'
    negate_next = False

    for token in doc:
        if token.is_space or token.is_punct:
            continue

        lemma = token.lemma_.strip().lower()
        if not lemma:
            continue

        if lemma in negation_words:
            negate_next = True
            continue

        if negate_next:
            if lemma not in all_stopwords and len(lemma) > 2:
                tokens.append(f"neg_{lemma}")
            negate_next = False
            continue

        if lemma == "neg":
            continue

        if lemma not in all_stopwords and len(lemma) > 2:
            tokens.append(lemma)

    return " ".join(tokens)

# =======================
# Utilitaires
# =======================
def print_top_words(text, top_n=20):
    words = [w for w in text.split() if w not in CUSTOM_STOPWORDS and w != "neg"]
    counter = Counter(words)
    top_words = counter.most_common(top_n)
    print("Top 20 mots les plus fréquents")
    for w, c in top_words:
        print(f"{w:<20} : {c}")
    return counter

def generate_wordcloud(text):
    wc = WordCloud(
        width=800, height=400, background_color='white',
        max_words=200, colormap='viridis',
        stopwords=WC_STOPWORDS
    ).generate(text)
    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(OUTPUT_WORDCLOUD)
    plt.close()

def generate_lda(texts, num_topics=5):
    # Filtrage sécurité
    cleaned = [" ".join([w for w in t.split() if w not in CUSTOM_STOPWORDS and w != "neg"]) for t in texts]

    tokenized = [t.split() for t in cleaned]
    dictionary = corpora.Dictionary(tokenized)
    corpus = [dictionary.doc2bow(t) for t in tokenized]
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10, random_state=42)
    topics = lda_model.show_topics(num_topics=num_topics, num_words=6, formatted=False)

    print("Thèmes détectés (LDA) :")
    for i, topic in topics:
        print(f" - Thème {i+1} : {', '.join([w for w, _ in topic])}")

    # Visualisation très simple : barres par thème (somme des poids)
    plt.figure(figsize=(10, 5))
    for i, topic in topics:
        words = [w for w, _ in topic]
        weights = [w_ for _, w_ in topic]
        plt.barh([f"Thème {i+1} : {w}" for w in words], weights)
    plt.title("Thèmes LDA - top mots")
    plt.tight_layout()
    plt.savefig(OUTPUT_LDA_IMG)
    plt.close()

    return [{"theme": i+1, "words": [w for w, _ in topic]} for i, topic in topics]

def sentiment_stats(texts):
    polarities = [TextBlob(t).sentiment.polarity for t in texts]
    pos = sum(p > 0.2 for p in polarities)
    neu = sum(-0.2 <= p <= 0.2 for p in polarities)
    neg = sum(p < -0.2 for p in polarities)
    total = len(polarities)
    print("Distribution sentiments TextBlob")
    print(f" - Positifs : {pos} ({pos/total:.1%})")
    print(f" - Neutres  : {neu} ({neu/total:.1%})")
    print(f" - Négatifs : {neg} ({neg/total:.1%})")

    # Histogramme
    plt.figure(figsize=(10,5))
    plt.hist(polarities, bins=20, color='cornflowerblue', edgecolor='black')
    plt.title("Distribution des sentiments")
    plt.xlabel("Polarité")
    plt.ylabel("Nombre d'avis")
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(OUTPUT_SENTIMENT_HIST)
    plt.close()

    return {"positif": pos, "neutre": neu, "negatif": neg, "total": total}

def save_report(stats, top_words_counter, lda_topics):
    # Filtrage sécurité pour le CSV
    top20_filtered = [(w, c) for w, c in top_words_counter.items() if w not in CUSTOM_STOPWORDS and w != "neg"]
    top20_filtered = sorted(top20_filtered, key=lambda x: x[1], reverse=True)[:20]

    df_stats = pd.DataFrame({
        "nb_avis": [stats["total"]],
        "sentiments_positif": [stats["positif"]],
        "sentiments_neutre": [stats["neutre"]],
        "sentiments_negatif": [stats["negatif"]],
        "top20_mots": ["; ".join([f"{w}:{c}" for w, c in top20_filtered])],
        "lda_resume": [" | ".join([f"Thème {t['theme']} : {', '.join(t['words'])}" for t in lda_topics])]
    })
    df_stats.to_csv(OUTPUT_STATS, index=False)
    print(f"✅ Statistiques CSV sauvegardées : {OUTPUT_STATS}")

# =======================
# Main
# =======================
def main():
    print("📥 Lecture du fichier :", INPUT_CSV)
    df = pd.read_csv(INPUT_CSV)
    print(f"{len(df)} avis chargés")

    print("🧼 Nettoyage & lemmatisation + gestion négation (patch custom stopwords)...")
    df['commentaire_preprocessed'] = df['commentaire'].apply(preprocess_text_with_negation)

    # Filtrage sécurité final
    df['commentaire_preprocessed'] = df['commentaire_preprocessed'].apply(
        lambda t: " ".join([w for w in t.split() if w not in CUSTOM_STOPWORDS and w != "neg"])
    )

    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Fichier nettoyé sauvegardé : {OUTPUT_CSV}")

    series_clean = df['commentaire_preprocessed'].dropna()

    all_text = " ".join(series_clean)
    top_words_counter = print_top_words(all_text)

    generate_wordcloud(all_text)
    print(f"✅ Wordcloud sauvegardé : {OUTPUT_WORDCLOUD}")

    lda_topics = generate_lda(series_clean)
    print(f"✅ Graphique LDA sauvegardé : {OUTPUT_LDA_IMG}")

    stats = sentiment_stats(series_clean)
    print(f"✅ Histogramme des sentiments sauvegardé : {OUTPUT_SENTIMENT_HIST}")

    save_report(stats, top_words_counter, lda_topics)

    print("✅ Analyse terminée")

if __name__ == "__main__":
    main()
