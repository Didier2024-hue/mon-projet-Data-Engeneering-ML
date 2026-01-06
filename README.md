# 📊 Analyse de Satisfaction Client - Trustpilot Data Engineering Project

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

---

## 🎯 Objectifs du Projet

Projet réalisé dans le cadre de la formation **Data Engineer** chez **DataScientest**. Ce projet propose une approche **end-to-end** pour extraire, structurer, enrichir, analyser et modéliser des avis clients issus de Trustpilot. L'objectif est de détecter automatiquement la satisfaction client, d'identifier les points d'amélioration des entreprises et de créer un outil de veille concurrentielle multi-source.

| Phase | Objectif | Résultat obtenu |
|-------|----------|-----------------|
| 🔎 **Collecte** | Scraping automatisé Trustpilot + Wikipedia | 66k+ avis collectés |
| 🗃️ **Stockage** | Architecture duale MongoDB + PostgreSQL | Données centralisées et tracées |
| 🌐 **Enrichissement** | Métadonnées entreprises (CA, SIREN, secteur...) | Contexte métier complet |
| 🛠️ **Préparation** | Nettoyage, standardisation, annotation BERT | 58 328 avis exploitables |
| 🤖 **Modélisation** | Benchmarking BERT, TF-IDF + SVM, LinearSVC | F1-score ≈ 0.75 |
| 🚀 **Production** | API FastAPI + Streamlit + Docker | 17 conteneurs, 78% tests |
| 🔧 **MLOps** | Airflow + GitLab CI/CD + Monitoring | Pipeline industrialisé |

---

## 🏢 Entreprises Analysées

L'analyse s'est focalisée sur 4 acteurs majeurs, choisis pour leur notoriété et diversité sectorielle :

| Entreprise | Secteur | Avis Collectés | Enjeux Principaux |
|------------|---------|----------------|-------------------|
| **Tesla** | Automobile high-tech / Énergie verte | 21 743 | Qualité produit, innovation, service après-vente |
| **Temu** | E-commerce grand public | 32 220 | Rapport qualité-prix, délais de livraison |
| **Chronopost** | Logistique et transport | 3 545 | Ponctualité, traitement des réclamations |
| **Vinted** | E-commerce C2C | 308 | Expérience utilisateur, confiance entre particuliers |

**Total :** 58 328 avis analysés

---

## 🏗️ Architecture du Projet

Le projet suit une architecture **end-to-end**, couvrant l'ensemble du flux de données :

```mermaid
graph TD
    A[Trustpilot Scraping] --> B[MongoDB]
    C[Wikipedia API] --> D[PostgreSQL]
    B --> E[Preprocessing NLP]
    D --> E
    E --> F[Modelisation ML]
    F --> G[API FastAPI]
    F --> H[Dashboard Streamlit]
    G --> I[Docker Containers]
    H --> I
    I --> J[Monitoring Grafana]
    K[Airflow] --> A
    K --> E
    L[GitLab CI/CD] --> I
Composants Clés :
Collecte : Scraping automatisé Trustpilot + API Wikipedia

Stockage : MongoDB (avis) + PostgreSQL (métadonnées)

ML/NLP : Pipeline complet avec BERT, LinearSVC

Exposition : API FastAPI + Interface Streamlit

MLOps : Airflow + GitLab + Prometheus/Grafana

⚙️ Enchaînement des Scripts
Étape 1 – Collecte des Données
https://github.com/user-attachments/assets/c989627d-02de-4fd6-b3f7-25b34d36ee51

Scraping Trustpilot : python scripts/scraping/cde_scrap_new.py

API Wikipedia : python scripts/scraping/cde_scrap_wiki.py

Chargement MongoDB : python scripts/scraping/creation_mongodb.py

Chargement PostgreSQL : python scripts/scraping/creation_postgre.py

Étape 2 – Préparation ML
https://github.com/user-attachments/assets/530c8d02-807f-44de-b307-6c9bcb1e0500

Snapshot MongoDB : python scripts/ml/snapshot_data.py

Annotation BERT : python scripts/ml/sentiment_analysis.py

Nettoyage : python scripts/ml/clean_data.py

Préprocessing NLP : python scripts/ml/preprocessing_demo_ml.py

Étape 3 – Modélisation
Benchmarking : python scripts/ml/train_dual_models.py

Sérialisation : python scripts/ml/save_model.py

Suivi MLflow : python scripts/ml/mlflow_tracking.py

🤖 Machine Learning & NLP
Pipeline de Traitement
Extraction : Export des avis bruts depuis MongoDB

Annotation BERT : Génération automatique des labels (sentiment & notes 1-5)

Nettoyage : Suppression doublons, outliers, commentaires non exploitables

NLP Avancé : Lemmatisation, gestion négations, normalisation

Vectorisation : TF-IDF pour les modèles classiques

Benchmarking : Comparaison de 3 modèles sur 2 tâches

Résultats du Benchmarking
Tâche	Modèle	Accuracy	F1-score (macro)
Sentiment	LogisticRegression	82.62%	0.7537
Sentiment	LinearSVC	85.06%	0.7546
Sentiment	RandomForest	81.40%	0.6445
Note	LogisticRegression	70.73%	0.4697
Note	LinearSVC	80.43%	0.4949
Note	RandomForest	79.48%	0.3594
Modèle retenu : LinearSVC (meilleures performances sur les deux tâches)

Visualisations ML
https://github.com/user-attachments/assets/f1f1128f-60ee-4f3b-9fa6-b989b46915e4

🚀 API & Déploiement
Architecture API
https://github.com/user-attachments/assets/b19fae52-a02c-40a4-98ec-076a3bed25dd

Composants :
FastAPI : Endpoints REST pour consultation, prédiction, export

JWT Authentication : 3 modes (Off, Partial, Full)

Streamlit : Dashboard interactif + tester ML

Docker : 17 conteneurs isolés

Tests : 78% coverage avec Pytest

Exemple d'utilisation API :
python
import requests

# Authentification
response = requests.post("http://localhost:8000/token", 
                         data={"username": "user", "password": "pass"})
token = response.json()["access_token"]

# Prédiction
headers = {"Authorization": f"Bearer {token}"}
data = {"text": "Produit excellent mais livraison tardive"}
response = requests.post("http://localhost:8000/predict/sentiment", 
                         json=data, headers=headers)
print(response.json())
🔧 MLOps & Industrialisation
Orchestration (Airflow)
DAGs automatisés : Scraping → Nettoyage → Entraînement → Déploiement

Mode manuel : Pour tests et re-lancements contrôlés

Monitoring : Suivi des exécutions et alertes

CI/CD (GitLab)
Pipeline automatisé : Linting (flake8) + Tests API

Validation : Tests dans conteneur Docker avant déploiement

Versioning : Gestion du code et des modèles

Monitoring (Prometheus + Grafana)
Collecte métriques : Services, conteneurs, système

Dashboards temps réel : Visualisation des performances

Alerting : Notification pro-active des incidents

📊 Résultats Métier
Entreprise	Points Forts	Points Faibles	Recommandations
Tesla	Innovation Produit	Service Après-Vente	Investir dans l'expérience post-achat pour protéger l'image premium
Chronopost	Rapidité du réseau	Manque de flexibilité du dernier kilomètre	Améliorer le suivi en temps réel et les solutions de recours
Vinted	Force de la communauté	Lenteur dans l'arbitrage des litiges	Renforcer la confiance via une médiation plus juste et rapide
Temu	Prix bas	Écart attentes/réalité (qualité, délais)	Gérer les attentes et simplifier les retours
Insights Clés :
Polarisation forte : 75% des avis sont très positifs (5/5) ou très négatifs (1/5)

Thèmes récurrents : Livraison, service client, qualité produit

Mots influents :

Positifs : excellent, parfait, rapide, top

Négatifs : problème, dommage, impossible, attente

📁 Structure du Projet
text
trustpilot-analysis/
├── scripts/
│   ├── scraping/
│   │   ├── cde_scrap_new.py          # Scraping Trustpilot
│   │   ├── cde_scrap_wiki.py         # Scraping Wikipedia
│   │   ├── creation_mongodb.py       # Initialisation MongoDB
│   │   └── creation_postgre.py       # Initialisation PostgreSQL
│   ├── ml/
│   │   ├── snapshot_data.py          # Export MongoDB → CSV
│   │   ├── sentiment_analysis.py     # Annotation BERT
│   │   ├── clean_data.py             # Nettoyage données
│   │   ├── preprocessing_demo_ml.py  # Préprocessing NLP
│   │   ├── train_dual_models.py      # Entraînement modèles
│   │   └── mlflow_tracking.py        # Suivi expérimentations
│   └── api/
│       ├── main.py                   # FastAPI application
│       ├── auth.py                   # Authentification JWT
│       └── tests/                    # Tests automatisés
├── dashboard/
│   └── app_streamlit.py              # Interface Streamlit
├── mlops/
│   ├── dags/                         # Airflow DAGs
│   ├── .gitlab-ci.yml                # Pipeline CI/CD
│   └── monitoring/                   # Config Prometheus/Grafana
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.streamlit
│   ├── Dockerfile.mlflow
│   └── docker-compose.yml
├── data/
│   ├── raw/                          # Données brutes
│   ├── processed/                    # Données nettoyées
│   └── models/                       # Modèles sérialisés
├── notebooks/
│   └── analysis.ipynb                # Analyses exploratoires
├── requirements.txt
├── docker-compose.yml
└── README.md
🛠️ Installation
Prérequis
bash
python --version   # >= 3.9
docker --version   # >= 20.10
docker-compose --version
Installation Complète
bash
# 1. Clone du repository
git clone https://github.com/Didier2024-hue/trustpilot-analysis.git
cd trustpilot-analysis

# 2. Lancement des services Docker
docker-compose up -d

# 3. Installation des dépendances Python
pip install -r requirements.txt

# 4. Initialisation des bases de données
python scripts/scraping/creation_mongodb.py
python scripts/scraping/creation_postgre.py

# 5. Démarrage de l'application
python scripts/api/main.py
Accès aux Services
Service	URL	Port
FastAPI	http://localhost:8000	8000
Streamlit	http://localhost:8501	8501
MLflow	http://localhost:5000	5000
Grafana	http://localhost:3000	3000
Airflow	http://localhost:8080	8080
Variables d'Environnement
bash
cp .env.example .env
# Éditer .env avec vos configurations
👥 Équipe
Rôle	Nom	Contribution
Auteur	Didier J.	Développement complet du projet
Tuteur	Rémy D.	Encadrement technique
COO	Vincent L.	Supervision métier
Organisme	DataScientest	Formation Data Engineer
Promotion	2025 - Supply Chain & Satisfaction Client	
Contact : kiembraid@gmail.com
GitHub : Didier2024-hue

📄 Licence
Ce projet est un travail académique réalisé dans le cadre de la formation Data Engineer de DataScientest.
Distribué sous licence MIT - voir le fichier LICENSE pour plus de détails.

🔗 Liens Utiles
📚 Documentation API

📊 Dashboard Streamlit

🔬 MLflow Tracking

📈 Monitoring Grafana

🔄 Airflow DAGs
