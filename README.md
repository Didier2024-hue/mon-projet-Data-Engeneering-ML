# 📊 Analyse de la Satisfaction Client - Trustpilot Data Engineering Project

## 📋 Menu
- [🎯 Objectifs du Projet](#-objectifs-du-projet)
- [🏢 Entreprises Analysées](#-entreprises-analysées)
- [🏗️ Architecture du Projet](#️-architecture-du-projet)
- [⚙️ Enchaînement des Scripts](#️-enchaînement-des-scripts)
- [🤖 Machine Learning & NLP](#-machine-learning--nlp)
- [🚀 API & Déploiement](#-api--déploiement)
- [🔧 MLOps & Industrialisation](#️-mlops--industrialisation)
- [📊 Résultats Métier](#-résultats-métier)
- [📁 Structure du Projet](#-structure-du-projet)
- [🛠️ Installation](#️-installation)
- [👥 Équipe](#-équipe)
- [📄 Licence](#-licence)

---

## 🎯 Objectifs du Projet

Projet réalisé dans le cadre de la formation **Data Engineer** chez **DataScientest**. Cette solution end-to-end permet d'extraire, structurer, enrichir, analyser et modéliser des avis clients Trustpilot pour mesurer automatiquement la satisfaction client et identifier des insights actionnables.

**Objectifs principaux :**
- Automatiser la collecte et le traitement des avis clients
- Fournir des indicateurs de satisfaction en temps réel
- Identifier les points forts/faibles par entreprise
- Industrialiser la veille concurrentielle via une plateforme MLOps

**Synthèse des résultats :**
| Phase | Objectif | Résultat |
|-------|----------|----------|
| 🔎 **Collecte** | Scraping Trustpilot + Wikipedia | 66k+ avis collectés |
| 🗃️ **Stockage** | Architecture duale | MongoDB + PostgreSQL |
| 🌐 **Enrichissement** | Métadonnées entreprises | Contexte métier complet |
| 🛠️ **Préparation** | Nettoyage + annotation BERT | 58 328 avis exploitables |
| 🤖 **Modélisation** | Benchmark ML & NLP | F1-score ≈ 0.75 |
| 🚀 **Production** | API + Dashboard + Docker | 17 conteneurs, 78% tests |
| 🔧 **MLOps** | Pipeline industrialisé | Airflow + CI/CD + Monitoring |

---

## 🏢 Entreprises Analysées

| Entreprise | Secteur | Avis Collectés | Enjeux Principaux |
|------------|---------|----------------|-------------------|
| **Tesla** | Automobile / Énergie | 21 743 | Innovation, SAV, qualité produit |
| **Temu** | E-commerce B2C | 32 220 | Qualité perçue, délais livraison |
| **Chronopost** | Logistique | 3 545 | Ponctualité, gestion litiges |
| **Vinted** | Marketplace C2C | 308 | Confiance, expérience utilisateur |

**Total analysé :** 58 328 avis français

---

## 🏗️ Architecture du Projet

**Flux de données :**
Trustpilot Scraping → MongoDB (avis)
Wikipedia API → PostgreSQL (métadonnées)
↓
Préprocessing NLP → Modélisation ML
↓
API FastAPI → Dashboard Streamlit
↓
Docker Containers → Monitoring Grafana
↑
Airflow (orchestration) + GitLab CI/CD

text

**Composants clés :**
1. **Collecte** : Scraping automatisé + API Wikipedia
2. **Stockage** : MongoDB (avis JSON) + PostgreSQL (métadonnées)
3. **Traitement** : Pipeline NLP complet avec BERT
4. **Modélisation** : LinearSVC (85.06% accuracy sentiment)
5. **Exposition** : FastAPI + Streamlit conteneurisés
6. **MLOps** : Airflow + GitLab + Prometheus/Grafana

---


**Composants clés :**
1. **Collecte** : Scraping automatisé + API Wikipedia
2. **Stockage** : MongoDB (avis JSON) + PostgreSQL (métadonnées)
3. **Traitement** : Pipeline NLP complet avec BERT
4. **Modélisation** : LinearSVC (85.06% accuracy sentiment)
5. **Exposition** : FastAPI + Streamlit conteneurisés
6. **MLOps** : Airflow + GitLab + Prometheus/Grafana

---

## ⚙️ Enchaînement des Scripts

### Étape 1 – Collecte
```bash
python scripts/scraping/cde_scrap_new.py      # Scraping Trustpilot
python scripts/scraping/cde_scrap_wiki.py     # Données Wikipedia
python scripts/scraping/creation_mongodb.py   # Initialisation MongoDB
python scripts/scraping/creation_postgre.py   # Initialisation PostgreSQL


python scripts/ml/snapshot_data.py            # Export MongoDB → CSV
python scripts/ml/sentiment_analysis.py       # Annotation BERT
python scripts/ml/clean_data.py               # Nettoyage données
python scripts/ml/preprocessing_demo_ml.py    # Préprocessing NLP

python scripts/ml/train_dual_models.py        # Benchmarking modèles
python scripts/ml/save_model.py               # Sérialisation modèle
python scripts/ml/mlflow_tracking.py          # Suivi expérimentations

python scripts/ml/train_dual_models.py        # Benchmarking modèles
python scripts/ml/save_model.py               # Sérialisation modèle
python scripts/ml/mlflow_tracking.py          # Suivi expérimentations

---

## 🤖 Machine Learning & NLP
Pipeline de traitement :

Extraction des avis bruts depuis MongoDB

Annotation automatique avec BERT (sentiment + notes 1-5)

Nettoyage (doublons, outliers, textes non exploitables)

Préprocessing NLP (lemmatisation, négations, normalisation)

Vectorisation TF-IDF

Benchmarking de 3 modèles sur 2 tâches

Résultats du benchmarking :

Tâche	Modèle	Accuracy	F1-score (macro)
Sentiment	LogisticRegression	82.62%	0.7537
Sentiment	LinearSVC	85.06%	0.7546
Sentiment	RandomForest	81.40%	0.6445
Note	LogisticRegression	70.73%	0.4697
Note	LinearSVC	80.43%	0.4949
Note	RandomForest	79.48%	0.3594
Modèle retenu : LinearSVC - Meilleures performances sur les deux tâches
