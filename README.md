📊 Analyse de la Satisfaction Client
Trustpilot – Data Engineering & MLOps Project
📋 Menu

🎯 Objectifs du projet

🏢 Entreprises analysées

🏗️ Architecture du projet

⚙️ Enchaînement des scripts

🤖 Machine Learning & NLP

🚀 API & Déploiement

🔧 MLOps & Industrialisation

📊 Résultats métier

📁 Structure du projet

🛠️ Installation

👥 Équipe

🎯 Objectifs du projet

Projet réalisé dans le cadre de la formation Data Engineer chez DataScientest.
Ce projet met en œuvre une approche end-to-end visant à extraire, structurer, enrichir, analyser et modéliser des avis clients issus de Trustpilot.

Les objectifs principaux sont :

mesurer automatiquement la satisfaction client ;

identifier les points forts et irritants par entreprise ;

fournir un outil de veille concurrentielle multi-entreprises, industrialisé et déployable.

Phase	Objectif	Résultat
🔎 Collecte	Scraping Trustpilot + enrichissement Wikipedia	66 000+ avis collectés
🗃️ Stockage	MongoDB + PostgreSQL	Données centralisées et historisées
🌐 Enrichissement	Métadonnées entreprises (secteur, CA, SIREN…)	Contexte métier enrichi
🛠️ Préparation	Nettoyage, standardisation, annotation BERT	58 328 avis exploitables
🤖 Modélisation	Benchmark ML & NLP	F1-score ≈ 0.75
🚀 Production	API FastAPI + Streamlit + Docker	17 conteneurs, 78 % de couverture de tests
🔧 MLOps	Airflow + CI/CD + Monitoring	Pipeline industrialisé
🏢 Entreprises analysées

L’étude porte sur quatre entreprises représentatives de secteurs variés :

Entreprise	Secteur	Avis collectés	Enjeux principaux
Tesla	Automobile / Énergie	21 743	Innovation, SAV, qualité produit
Temu	E-commerce B2C	32 220	Qualité perçue, délais
Chronopost	Logistique	3 545	Ponctualité, gestion des litiges
Vinted	Marketplace C2C	308	Confiance et expérience utilisateur

Total analysé : 58 328 avis

🏗️ Architecture du projet

Le projet suit une architecture end-to-end, couvrant l’ensemble du cycle de vie de la donnée.

graph TD
    A[Trustpilot Scraping] --> B[MongoDB]
    C[Wikipedia API] --> D[PostgreSQL]
    B --> E[Preprocessing NLP]
    D --> E
    E --> F[Modélisation ML]
    F --> G[API FastAPI]
    F --> H[Dashboard Streamlit]
    G --> I[Docker Containers]
    H --> I
    I --> J[Monitoring Grafana]
    K[Airflow] --> A
    K[Airflow] --> E
    L[GitLab CI/CD] --> I

Composants clés

Collecte : Scraping automatisé Trustpilot + API Wikipedia

Stockage : MongoDB (avis) et PostgreSQL (métadonnées entreprises)

Traitement ML / NLP : BERT, TF-IDF, LinearSVC

Exposition : API FastAPI et interface Streamlit

MLOps : Airflow, GitLab CI/CD, Prometheus, Grafana

⚙️ Enchaînement des scripts
Étape 1 – Collecte des données

Scraping Trustpilot

python scripts/scraping/cde_scrap_new.py


Enrichissement Wikipedia

python scripts/scraping/cde_scrap_wiki.py


Initialisation MongoDB

python scripts/scraping/creation_mongodb.py


Initialisation PostgreSQL

python scripts/scraping/creation_postgre.py

Étape 2 – Préparation ML

Snapshot MongoDB

Annotation automatique BERT

Nettoyage et filtrage

Préprocessing NLP avancé

Étape 3 – Modélisation

Entraînement et benchmarking

Sérialisation des modèles

Tracking des expériences avec MLflow

🤖 Machine Learning & NLP
Pipeline de traitement

Extraction des avis bruts depuis MongoDB

Annotation automatique du sentiment via BERT

Nettoyage (doublons, outliers, bruit)

Préprocessing NLP (lemmatisation, négations, normalisation)

Vectorisation TF-IDF

Benchmarking multi-modèles

Résultats du benchmarking
Tâche	Modèle	Accuracy	F1-score (macro)
Sentiment	Logistic Regression	82.62 %	0.7537
Sentiment	LinearSVC	85.06 %	0.7546
Sentiment	Random Forest	81.40 %	0.6445
Note	Logistic Regression	70.73 %	0.4697
Note	LinearSVC	80.43 %	0.4949
Note	Random Forest	79.48 %	0.3594

Modèle retenu : LinearSVC

🚀 API & Déploiement
Composants

FastAPI : endpoints REST (consultation, prédiction, export)

Authentification JWT : modes Off / Partial / Full

Streamlit : dashboard interactif

Docker : 17 conteneurs isolés

Tests : Pytest – 78 % de couverture

Exemple d’appel API
import requests

response = requests.post(
    "http://localhost:8000/token",
    data={"username": "user", "password": "pass"}
)

token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

data = {"text": "Produit excellent mais livraison tardive"}
response = requests.post(
    "http://localhost:8000/predict/sentiment",
    json=data,
    headers=headers
)

print(response.json())

🔧 MLOps & Industrialisation
Orchestration – Airflow

DAGs automatisés : Scraping → Nettoyage → Entraînement → Déploiement

Exécution contrôlée et relançable

Suivi des logs et alertes

CI/CD – GitLab

Linting (flake8)

Tests API automatisés

Validation avant déploiement Docker

Monitoring

Prometheus : collecte des métriques

Grafana : dashboards temps réel

Alerting : détection proactive d’incidents

📊 Résultats métier
Entreprise	Points forts	Points faibles	Recommandations
Tesla	Innovation	SAV	Renforcer l’expérience post-achat
Chronopost	Réseau rapide	Dernier kilomètre	Améliorer le suivi et les recours
Vinted	Communauté	Gestion des litiges	Accélérer l’arbitrage
Temu	Prix	Attentes client	Clarifier l’offre et les retours

Insights clés

Forte polarisation : 75 % des avis sont notés 1/5 ou 5/5

Thèmes récurrents : livraison, service client, qualité produit

📁 Structure du projet
trustpilot-analysis/
├── scripts/
├── dashboard/
├── mlops/
├── docker/
├── data/
├── notebooks/
├── requirements.txt
├── docker-compose.yml
└── README.md

🛠️ Installation
Prérequis

Python ≥ 3.9

Docker ≥ 20.10

Installation
git clone https://github.com/Didier2024-hue/trustpilot-analysis.git
cd trustpilot-analysis
docker-compose up -d
pip install -r requirements.txt

👥 Équipe
Rôle	Nom	Contribution
Auteur	Didier J.	Développement complet
Tuteur	Rémy D.	Encadrement technique
COO	Vincent L.	Supervision métier
Organisme	DataScientest	Formation Data Engineer
📄 Licence

Projet académique réalisé dans le cadre de la formation Data Engineer – DataScientest.
Licence MIT.
