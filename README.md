# 🟩🟨🟥 Analyse de la Satisfaction Client – Trustpilot 🟥🟨🟩

Projet réalisé dans le cadre de la formation **Data Scientist** chez **DataScientest**. Ce projet propose une approche de bout en bout pour extraire, structurer, enrichir, analyser et modéliser des avis clients issus de Trustpilot. L'objectif est de détecter automatiquement la satisfaction client, d'identifier les points d'amélioration des entreprises et de créer un outil de veille concurrentielle multi-source.

---

## 🗂 Menu

1. [Objectifs du Projet](#-objectifs-du-projet)
2. [Architecture du Projet](#-architecture-du-projet)
3. [Enchaînement des Scripts](#-enchaînement-des-scripts)
4. [Résultats et Visualisations](#-résultats-et-visualisations)
5. [Structure du Projet](#-structure-du-projet)
6. [Installation](#-installation)
7. [Auteur](#-auteur)

---

## 🎯 Objectifs du Projet

| Phase | Objectif | Résultat obtenu |
|-------|----------|-----------------|
| 🔎 Scraping Trustpilot | Collecte automatisée d'avis clients sur 4 entreprises | 10 215 avis bruts collectés |
| 🗃️ Stockage | Insertion dans MongoDB (NoSQL) et PostgreSQL (relationnel) | Données centralisées et tracées |
| 🌐 Enrichissement Wikipedia | Extraction de métadonnées sociétés (fondateur, CA...) | Données pour 4 entreprises |
| 🛠️ Préparation des données | Nettoyage, standardisation, calcul de métriques | 7 784 commentaires nettoyés |
| 🤖 Analyse de Sentiment (BERT) | Auto-labeling des sentiments à partir du texte | ≈ 8 000 avis annotés |
| 📊 Modélisation Machine Learning | Prédiction de la polarité et de la note de satisfaction | F1-score (sentiment) ≈ 0.70 |

---

## 🛠️ Architecture du Projet

Schema général: Trustpilot → Python Scraper → JSON → PostgreSQL / MongoDB → Machine Learning

![Schema général](https://github.com/user-attachments/assets/b19fae52-a02c-40a4-98ec-076a3bed25dd)

---

## ⚙️ Enchaînement des Scripts

### Étape 1 – Scraping Trustpilot

![Scraping Trustpilot](https://github.com/user-attachments/assets/c989627d-02de-4fd6-b3f7-25b34d36ee51)

1. Scraping des avis Trustpilot (par société) : `python scripts/scraping/cde_scrap.py`
2. Insertion dans PostgreSQL : `python scripts/scraping/insert_postgre.py`
3. Insertion dans MongoDB : `python scripts/scraping/insert_mongodb.py`

➡️ Scraping des données Vinted, Chronopost, Tesla, Vinted : 10 215 avis bruts collectés

### Étape 2 – Enrichissement Wikipedia

1. Scraping des infobox Wikipedia (logo, fondateur, CA, etc.) : `python scripts/wiki/cde_scrap_wiki.py`
2. Insertion dans PostgreSQL : `python scripts/wiki/cde_insert_wiki.py`

➡️ Vue unifiée générée automatiquement : `vue_societes_wiki_harmonisee`
<br>
<br>
### Étape 3 – Snapshot MongoDB → CSV

![Architecture technique ML](https://github.com/user-attachments/assets/530c8d02-807f-44de-b307-6c9bcb1e0500)

`python scripts/ml/snapshot_data.py`

➡️ Exporte les données nettoyées vers `export_trustpilot_avis_trustpilot.csv`, `export_trustpilot_societe.csv`

### Étape 4 – Nettoyage des Données

`python scripts/ml/clean_data.py`

| Étape | Avis restants |
|-------|---------------|
| Chargement initial | 7 936 |
| Doublons supprimés | 7 934 |
| Outliers extrêmes | 7 784 |
| Emojis-only retirés | 7 783 |

➡️ Fichier généré : `clean_avis_avec_sentiments.csv`

### Étape 5 – Analyse de Sentiments (BERT)

`python scripts/ml/sentiment_analysis.py`

Utilise : `nlptown/bert-base-multilingual-uncased-sentiment`

➡️ Fichier généré : `avis_avec_sentiments.csv`

### Étape 6 – Prétraitement Linguistique

`python scripts/ml/preprocessing.py`

➡️ Fichier généré : `preprocess_clean_avis.csv`

### Étape 7 – Modélisation Machine Learning

`python scripts/ml/train_dual_models.py`

| Modèle | Sentiment (F1) | Note (F1) |
|--------|----------------|-----------|
| LogisticRegression | **0.7018** ✅ | 0.4320 |
| LinearSVC | 0.6891 | 0.4487 |
| RandomForest | 0.5581 | \~0.40 |

➡️ Modèle retenu : LogisticRegression

---

## 📊 Résultats et Visualisations

### Répartition des Scores (BERT)

| Score BERT | Volume | Pourcentage |
|------------|--------|-------------|
| 1 | 3 134 | 40.3 % |
| 5 | 2 754 | 35.4 % |
| 3 | 605 | 7.8 % |

➡️ Polarisation forte : plus de 75% des avis sont très positifs ou très négatifs.

### Thèmes LDA détectés

| Thème | Mots-clés |
|-------|-----------|
| Commande & réception | colis, commande, bien |
| Livraison & relais colis | livraison, point, livreur |
| Service / relation client | service, vendeur, article |
| Satisfaction | rapide, bon, parfait |
| Litiges & support client | problème, contacter, remboursement |

### Mots Influents (LogisticRegression)

➕ Positifs : excellent, parfait, rapide, top

➖ Négatifs : problème, dommage, impossible, attente

---

## 📁 Structure du Projet

![Structure du Projet](https://github.com/user-attachments/assets/f1f1128f-60ee-4f3b-9fa6-b989b46915e4)

---

## 🚀 Installation

Prérequis
bash
Copy code
python --version   # >= 3.9
docker --version   # >= 20.10


Clone & Démarrage
bash
Copy code
git clone https://github.com/votreuser/trustpilot-analysis.git
cd trustpilot-analysis


Lancer les bases
docker-compose up -d


Installer les dépendances
pip install -r requirements.txt


👤 Auteur
🎓 Formation : Data Engineer – DataScientest

📧 Email : kiembraid@gmail.com

🔗 GitHub : Didier2024-hue

📄 Licence
Ce projet est mis à disposition sous licence MIT.

Voir LICENSE pour plus de détails.


---
