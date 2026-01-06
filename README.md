# 📊 Analyse de la Satisfaction Client - Trustpilot Data Engineering Project

## 📋 Table des Matières
- [🎯 Objectifs du Projet](#-objectifs-du-projet)
- [🏢 Entreprises Analysées](#-entreprises-analysées)
- [🏗️ Architecture du Projet](#️-architecture-du-projet)
- [⚙️ Enchaînement des Scripts](#️-enchaînement-des-scripts)
- [🤖 Machine Learning & NLP](#-machine-learning--nlp)
- [🚀 API & Déploiement](#-api--déploiement)
- [🔧 MLOps & Industrialisation](#-mlops--industrialisation)
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

```
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
```

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
```

### Étape 2 – Préparation ML

```bash
python scripts/ml/snapshot_data.py            # Export MongoDB → CSV
python scripts/ml/sentiment_analysis.py       # Annotation BERT
python scripts/ml/clean_data.py               # Nettoyage données
python scripts/ml/preprocessing_demo_ml.py    # Préprocessing NLP
```

### Étape 3 – Modélisation

```bash
python scripts/ml/train_dual_models.py        # Benchmarking modèles
python scripts/ml/save_model.py               # Sérialisation modèle
python scripts/ml/mlflow_tracking.py          # Suivi expérimentations
```

---

## 🤖 Machine Learning & NLP

**Pipeline de traitement :**

1. Extraction des avis bruts depuis MongoDB
2. Annotation automatique avec BERT (sentiment + notes 1-5)
3. Nettoyage (doublons, outliers, textes non exploitables)
4. Préprocessing NLP (lemmatisation, négations, normalisation)
5. Vectorisation TF-IDF
6. Benchmarking de 3 modèles sur 2 tâches

**Résultats du benchmarking :**

| Tâche | Modèle | Accuracy | F1-score (macro) |
|-------|--------|----------|------------------|
| Sentiment | LogisticRegression | 82.62% | 0.7537 |
| Sentiment | LinearSVC | 85.06% | 0.7546 |
| Sentiment | RandomForest | 81.40% | 0.6445 |
| Note | LogisticRegression | 70.73% | 0.4697 |
| Note | LinearSVC | 80.43% | 0.4949 |
| Note | RandomForest | 79.48% | 0.3594 |

**Modèle retenu :** LinearSVC - Meilleures performances sur les deux tâches

---

## 🚀 API & Déploiement

**Stack technique :**
- **FastAPI** : API REST avec documentation auto-générée
- **JWT Authentication** : 3 modes (Off, Partial, Full)
- **Streamlit** : Dashboard interactif + testeur ML
- **Docker** : 17 conteneurs isolés (services découpés)
- **Tests** : 78% coverage avec Pytest

**Exemple d'utilisation :**

```python
import requests

# Authentification
response = requests.post("http://localhost:8000/token", 
                         data={"username": "user", "password": "pass"})
token = response.json()["access_token"]

# Prédiction de sentiment
headers = {"Authorization": f"Bearer {token}"}
data = {"text": "Produit excellent mais livraison tardive"}
response = requests.post("http://localhost:8000/predict/sentiment", 
                         json=data, headers=headers)
print(response.json())
```

---

## 🔧 MLOps & Industrialisation

### Orchestration (Airflow)
- **DAGs automatisés** : Scraping quotidien → Nettoyage → Entraînement
- **Planification** : Exécutions programmées et manuelles
- **Monitoring** : Logs détaillés et alertes d'erreurs

### CI/CD (GitLab)
- **Pipeline automatisé** : Linting (flake8) + Tests unitaires
- **Validation qualité** : Tests dans conteneur Docker isolé
- **Déploiement** : Build et push automatique des images

### Monitoring (Prometheus + Grafana)
- **Métriques temps réel** : CPU, mémoire, latence API
- **Dashboards** : Visualisation des performances système
- **Alerting** : Notifications proactives (Slack/Email)

---

## 📊 Résultats Métier

| Entreprise | Points Forts | Points Faibles | Recommandations |
|------------|--------------|----------------|-----------------|
| **Tesla** | Innovation technologique | Service après-vente | Investir dans l'expérience post-achat |
| **Chronopost** | Réseau étendu | Flexibilité dernier kilomètre | Améliorer le suivi en temps réel |
| **Vinted** | Communauté active | Lenteur arbitrage litiges | Accélérer la médiation |
| **Temu** | Prix attractifs | Écart attentes/réalité | Gérer les attentes clients |

**Insights clés :**

- 📈 **Polarisation marquée** : 75% des avis sont 1/5 ou 5/5
- 🔍 **Thèmes récurrents** : Livraison (35%), service client (28%), qualité (22%)
- 🎯 **Mots influents** :
  - ✅ Positifs : excellent, parfait, rapide, top, efficace
  - ❌ Négatifs : problème, attente, déçu, lent, cassé

---

## 📁 Structure du Projet

```
trustpilot-analysis/
├── scripts/
│   ├── scraping/
│   │   ├── cde_scrap_new.py
│   │   ├── cde_scrap_wiki.py
│   │   ├── creation_mongodb.py
│   │   └── creation_postgre.py
│   ├── ml/
│   │   ├── snapshot_data.py
│   │   ├── sentiment_analysis.py
│   │   ├── clean_data.py
│   │   ├── preprocessing_demo_ml.py
│   │   ├── train_dual_models.py
│   │   └── mlflow_tracking.py
│   └── api/
│       ├── main.py
│       ├── auth.py
│       └── tests/
├── dashboard/
│   └── app_streamlit.py
├── mlops/
│   ├── dags/
│   ├── .gitlab-ci.yml
│   └── monitoring/
├── docker/
│   ├── Dockerfile.api
│   ├── Dockerfile.streamlit
│   ├── Dockerfile.mlflow
│   └── docker-compose.yml
├── data/
│   ├── raw/
│   ├── processed/
│   └── models/
├── notebooks/
│   └── analysis.ipynb
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Installation

### Prérequis

```bash
python --version        # >= 3.9
docker --version        # >= 20.10
docker-compose version  # >= 2.0
```

### Installation rapide

```bash
# 1. Clone du repository
git clone https://github.com/Didier2024-hue/trustpilot-analysis.git
cd trustpilot-analysis

# 2. Lancement des services Docker
docker-compose up -d --build

# 3. Installation des dépendances Python
pip install -r requirements.txt

# 4. Initialisation des bases de données
python scripts/scraping/creation_mongodb.py
python scripts/scraping/creation_postgre.py

# 5. Démarrage de l'API
python scripts/api/main.py
```

### Accès aux services

| Service | URL | Port | Description |
|---------|-----|------|-------------|
| **FastAPI** | http://localhost:8000 | 8000 | API principale + documentation |
| **Streamlit** | http://localhost:8501 | 8501 | Dashboard interactif |
| **MLflow** | http://localhost:5000 | 5000 | Tracking expérimentations ML |
| **Grafana** | http://localhost:3000 | 3000 | Monitoring (admin/admin) |
| **Airflow** | http://localhost:8080 | 8080 | Orchestration workflows |

### Configuration

```bash
# Copier le template d'environnement
cp .env.example .env

# Éditer avec vos configurations
nano .env
```

---

## 👥 Équipe

| Rôle | Nom | Contribution |
|------|-----|--------------|
| **Auteur** | Didier J. | Développement complet du projet |
| **Tuteur** | Rémy D. | Encadrement technique et méthodologique |
| **COO** | Vincent L. | Supervision métier et stratégique |
| **Organisme** | DataScientest | Formation Data Engineer |

**Contact :**
- Email : kiembraid@gmail.com
- GitHub : [Didier2024-hue](https://github.com/Didier2024-hue)
- Formation : Data Engineer - Promotion 2025
- Spécialité : Supply Chain & Satisfaction Client

---

## 📄 Licence

Ce projet est un travail académique réalisé dans le cadre de la formation Data Engineer de DataScientest.

Distribué sous licence MIT - voir le fichier LICENSE pour plus de détails.

**Note :** Les données Trustpilot sont utilisées à des fins éducatives et respectent les conditions d'utilisation du site.

---

**Dernière mise à jour :** Janvier 2025  
**Statut du projet :** ✅ Production - MLOps Industrialisé

---

*DataScientest • Data Engineer • Promotion 2025*
