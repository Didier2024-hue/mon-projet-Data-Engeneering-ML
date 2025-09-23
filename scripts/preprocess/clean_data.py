import os
import json
import re
import emoji
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# === Chargement des variables d’environnement ===
load_dotenv()
BASE_DIR = os.getenv("BASE_DIR")
DATA_PROCESSED = os.getenv("DATA_PROCESSED")
DATA_REPORT = os.getenv("DATA_REPORT")

INPUT_PATH = os.path.join(DATA_PROCESSED, "export_sentiment_analysis.csv")
OUTPUT_PATH = os.path.join(DATA_PROCESSED, "export_clean_data.csv")
GRAPH_PATH = os.path.join(DATA_REPORT, "report_clean_data.png")
CSV_REPORT_PATH = os.path.join(DATA_PROCESSED, "stats_clean_data.csv")

# === Fonctions de nettoyage ===
def clean_text(text):
    if pd.isna(text):
        return np.nan
    text = re.sub(r'(?<!\w)(http\S+|www\S+|https\S+)(?!\w)', '', text, flags=re.MULTILINE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def count_emojis(text):
    if pd.isna(text):
        return 0
    return sum(1 for c in text if c in emoji.EMOJI_DATA)

def is_emoji_only(text):
    if pd.isna(text) or not text.strip():
        return False
    cleaned = re.sub(r'[^\w\s,.!?]', '', text)
    return len(cleaned.strip()) == 0 and any(c in emoji.EMOJI_DATA for c in text)

def handle_duplicates_missing(df):
    df['commentaire_clean'] = df['commentaire'].apply(clean_text)
    duplicates = df.duplicated(subset=['commentaire_clean'], keep='first')
    print(f"→ Doublons textuels détectés : {duplicates.sum()}")
    df = df.drop_duplicates(subset=['commentaire_clean'], keep='first')
    return df.drop(columns=['commentaire_clean'])

def handle_outliers(df, stats_log):
    if 'commentaire' not in df.columns:
        return df
    df['comment_length'] = df['commentaire'].str.len().fillna(0)
    stats = df['comment_length'].describe()
    print("→ Statistiques des longueurs de commentaire :")
    print(stats)
    stats_log.append(stats.to_dict())
    q1 = df['comment_length'].quantile(0.01)
    q99 = df['comment_length'].quantile(0.99)
    initial = len(df)
    df = df[(df['comment_length'] >= q1) & (df['comment_length'] <= q99)]
    print(f"→ Commentaires conservés après filtre : {len(df)}/{initial} ({(len(df)/initial):.2%})")
    return df.drop(columns=['comment_length'])

def create_metrics(df):
    print("→ Calcul des métriques sur les commentaires")
    df['nb_mots'] = df['commentaire'].apply(lambda x: len(str(x).split()))
    df['nb_emojis'] = df['commentaire'].apply(count_emojis)
    df['longueur_commentaire'] = df['commentaire'].apply(lambda x: len(str(x)))
    return df

def handle_emoji_only(df):
    print("→ Détection des commentaires composés uniquement d’emojis...")
    df['emoji_only'] = df['commentaire'].apply(is_emoji_only)
    count = df['emoji_only'].sum()
    print(f"→ Commentaires uniquement emojis supprimés : {count}")
    df = df[~df['emoji_only']]
    return df.drop(columns=['emoji_only'])

# === Fonction principale ===
def main():
    try:
        df = pd.read_csv(INPUT_PATH, dtype={'note_commentaire': str})
        print(f"✅ Données chargées : {len(df)} lignes")
    except Exception as e:
        print(f"❌ Erreur de chargement : {str(e)}")
        return

    expected_cols = ['auteur', 'date', 'commentaire', 'note_commentaire']
    if missing := [col for col in expected_cols if col not in df.columns]:
        print(f"❌ Colonnes manquantes : {missing}")
        return

    etapes = []
    lignes_restantes = []
    stats_details = []
    
    steps = [
        ("Nettoyage initial", lambda x: x.assign(commentaire=x['commentaire'].apply(clean_text))),
        ("Gestion des valeurs manquantes", lambda x: x.dropna(subset=['commentaire'])),
        ("Suppression des doublons", handle_duplicates_missing),
        ("Ajout des métriques", create_metrics),
        ("Filtrage des outliers", lambda x: handle_outliers(x, stats_details)),
        ("Suppression des commentaires emojis-only", handle_emoji_only)
    ]

    for name, step in steps:
        try:
            print(f"\n=== Étape : {name} ===")
            before = len(df)
            df = step(df)
            after = len(df)
            print(f"→ Lignes restantes après '{name}' : {after} (perte : {before - after})")
            etapes.append(name)
            lignes_restantes.append(after)
        except Exception as e:
            print(f"❌ Erreur dans l'étape {name} : {str(e)}")
            return

    # === Sauvegarde des données nettoyées ===
    df.to_csv(OUTPUT_PATH, index=False, encoding='utf-8-sig')

    # === Génération du graphique PNG ===
    plt.figure(figsize=(10, 6))
    plt.plot(etapes, lignes_restantes, marker="o", linestyle="-", color="royalblue")
    plt.title("Évolution du nombre de lignes après chaque étape de nettoyage")
    plt.xlabel("Étapes de nettoyage")
    plt.ylabel("Nombre de lignes restantes")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(GRAPH_PATH, dpi=300)
    print(f"\n📊 Graphique généré : {GRAPH_PATH}")

    # === Rapport statistique au format CSV ===
    rows_stats = []
    for i, etape in enumerate(etapes):
        row = {
            "étape": etape,
            "lignes_restantes": lignes_restantes[i],
            "perte_depuis_etape_prec": lignes_restantes[i-1] - lignes_restantes[i] if i > 0 else 0
        }
        if i == 4 and stats_details:  # Ajoute les stats de longueur
            row.update(stats_details[0])  # count, mean, std, min, 25%, 50%, 75%, max
        rows_stats.append(row)

    df_report = pd.DataFrame(rows_stats)
    df_report.to_csv(CSV_REPORT_PATH, index=False, encoding="utf-8-sig")
    print(f"📁 Rapport CSV généré : {CSV_REPORT_PATH}")
    print(f"\n✅ Données finales sauvegardées dans : {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
