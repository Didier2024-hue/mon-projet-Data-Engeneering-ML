# 📊 Analyse de la Satisfaction Client - Trustpilot Data Engineering Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production-success.svg)

**Supply Chain - Satisfaction des clients • Promotion 2025**

</div>

---

## 📋 Table des Matières
- [🎯 Résumé Exécutif](#-résumé-exécutif)
- [🏢 Périmètre & Entreprises Analysées](#-périmètre--entreprises-analysées)
- [🏗️ Architecture Fonctionnelle Globale](#️-architecture-fonctionnelle-globale)
- [📦 Partie 1 : Collecte des Données](#-partie-1--collecte-des-données)
- [🗄️ Partie 2 : Stockage](#️-partie-2--stockage)
- [🤖 Partie 3 : Machine Learning & NLP](#-partie-3--machine-learning--nlp)
- [🚀 Partie 4 : API & Déploiement Docker](#-partie-4--api--déploiement-docker)
- [🔧 Partie 5 : MLOps & Industrialisation](#-partie-5--mlops--industrialisation)
- [📊 Résultats Métier](#-résultats-métier)
- [⚙️ Guide d'Installation](#️-guide-dinstallation)
- [📁 Structure du Projet](#-structure-du-projet)
- [👥 Équipe](#-équipe)
- [📄 Licence](#-licence)

---

## 🎯 Résumé Exécutif

Ce projet analyse la satisfaction client à partir des avis Trustpilot. Il couvre toute la chaîne de traitement, de la collecte des données brutes via web scraping à leur exposition via une API sécurisée, en passant par la modélisation Machine Learning.

### 🔍 Collecte & Stockage
Collecte automatisée de **66k+ avis Trustpilot** et données Wikipédia, stockés dans une architecture duale **MongoDB** (NoSQL) et **PostgreSQL** (SQL).

### 🧠 Analyse & Machine Learning
Pipeline NLP complet avec un dataset final de **58k+ avis**. Benchmarking de modèles (BERT, TF-IDF + SVM) pour la détection de sentiments et la prédiction de notes.

### 🌐 API & Déploiement
Développement d'une **API FastAPI** sécurisée par JWT, conteneurisée avec Docker et couverte à **78%** par des tests automatisés.

### ⚙️ MLOps & Supervision
Orchestration des pipelines avec **Airflow**, CI/CD avec **GitLab**, et supervision continue de la plateforme avec **Grafana** et **Prometheus**.

---

## 🏢 Périmètre & Entreprises Analysées

L'analyse s'est focalisée sur quatre acteurs majeurs, choisis pour leur notoriété et leur diversité sectorielle, afin de permettre une **analyse comparative intersectorielle**.

<div align="center">

```mermaid
pie title Répartition des Avis Clients par Entreprise
    "Temu (E-commerce)" : 32220
    "Tesla (Automobile)" : 30882
    "Chronopost (Logistique)" : 3545
    "Vinted (Marketplace)" : 217
```

</div>

| Entreprise | Secteur | Avis Collectés | Enjeux Principaux |
|------------|---------|----------------|-------------------|
| **Tesla** | Automobile high-tech / Énergie verte | 30 882 | Innovation, qualité produit, service après-vente |
| **Temu** | E-commerce grand public | 32 220 | Rapport qualité-prix, délais livraison, satisfaction |
| **Chronopost** | Logistique et transport | 3 545 | Ponctualité, traitement des réclamations |
| **Vinted** | E-commerce C2C (particuliers) | 217 | Expérience utilisateur, confiance entre particuliers |

**Total analysé :** 66 864 avis collectés → **58 328 avis exploitables après nettoyage**

---

## 🏗️ Architecture Fonctionnelle Globale

Le projet suit une architecture **end-to-end**, couvrant l'ensemble du flux de données, de la collecte à la mise en production supervisée.

```mermaid
graph LR
    A[1. Collecte<br/>Trustpilot + Wikipedia] --> B[2. Stockage<br/>MongoDB + PostgreSQL]
    B --> C[3. Préparation & NLP<br/>Nettoyage + Enrichissement]
    C --> D[4. Modélisation<br/>BERT + SVM + MLflow]
    D --> E[5. Exposition<br/>FastAPI + Streamlit]
    E --> F[6. MLOps<br/>Airflow + CI/CD + Monitoring]
    F -.Feedback.-> A
    
    style A fill:#e1f5ff
    style B fill:#fff4e1
    style C fill:#e8f5e9
    style D fill:#f3e5f5
    style E fill:#fce4ec
    style F fill:#fff3e0
```

### Les 6 Étapes du Pipeline

| Étape | Composant | Description |
|-------|-----------|-------------|
| **1️⃣ Collecte** | Scraping automatisé | Avis Trustpilot + données entreprises Wikipedia |
| **2️⃣ Stockage** | Architecture bi-base | MongoDB (avis) + PostgreSQL (métadonnées) |
| **3️⃣ Préparation** | Pipeline NLP | Nettoyage, normalisation, enrichissement sémantique |
| **4️⃣ Modélisation** | ML Benchmarking | BERT, SVM avec suivi MLflow |
| **5️⃣ Exposition** | API + Dashboard | FastAPI sécurisée + Streamlit conteneurisés |
| **6️⃣ MLOps** | Orchestration | Airflow + GitLab CI/CD + Grafana/Prometheus |

---

## 📦 Partie 1 : Collecte des Données

Cette première étape consiste à récupérer les données de sources hétérogènes.

```mermaid
graph TB
    subgraph Sources
        A[Trustpilot<br/>Avis Clients]
        B[Wikipedia<br/>Données Entreprises]
    end
    
    subgraph Collecte
        C[Script Python<br/>Web Scraping]
        D[API Wikipedia<br/>REST]
    end
    
    subgraph Stockage
        E[(MongoDB<br/>Avis JSON)]
        F[(PostgreSQL<br/>Métadonnées)]
    end
    
    A -->|robots.txt<br/>respecté| C
    B -->|Requêtes<br/>mensuelles| D
    C -->|Insertion<br/>quotidienne| E
    D -->|Schéma UML| F
    
    style A fill:#ff9800
    style B fill:#2196f3
    style E fill:#4caf50
    style F fill:#9c27b0
```

### 🌐 Avis Clients (Trustpilot)

- **Source principale** des données d'analyse
- Script Python automatisé collectant **quotidiennement** les avis en français
- Processus **résilient** : reprend là où il s'est arrêté
- Respect des contraintes du site (robots.txt)
- **Collecte historisée et horodatée**
- Stockage brut dans **MongoDB**

### 📚 Données Sociétales (Wikipedia)

- Collecte **mensuelle** via l'API Wikipedia
- Enrichissement avec informations structurelles (CA, SIREN, secteur, etc.)
- Offre un **contexte métier récent**
- Données structurées et normalisées
- Stockage dans **PostgreSQL**

---

## 🗄️ Partie 2 : Stockage

Cette seconde étape consiste à stocker les données de sources hétérogènes avec une architecture duale optimisée.

```mermaid
graph LR
    subgraph MongoDB
        A[Avis Clients<br/>Format JSON]
        B[Schéma Flexible<br/>schemaless]
        C[Opérations Rapides<br/>Grands Volumes]
    end
    
    subgraph PostgreSQL
        D[Métadonnées<br/>Entreprises]
        E[Schéma UML<br/>Normalisé]
        F[Backend MLflow<br/>Suivi Modèles]
    end
    
    style MongoDB fill:#4caf50
    style PostgreSQL fill:#9c27b0
```

### 🍃 MongoDB (Flexibilité Documentaire)

- **Stockage des avis clients** Trustpilot au format JSON
- **Schéma flexible** ("schemaless") pour ingérer les avis bruts sans perte d'information
- Optimisé pour des **opérations de lecture/écriture rapides** sur de grands volumes
- Idéal pour données non structurées et évolutives

### 🐘 PostgreSQL (Rigueur Relationnelle)

- **Stockage des métadonnées** des entreprises (Wikipedia)
- **Schéma UML normalisé** pour garantir la cohérence des données
- Utilisé comme **backend pour MLflow**, assurant le suivi fiable des modèles
- Garantit l'intégrité référentielle et les transactions ACID

---

## 🤖 Partie 3 : Machine Learning & NLP

Cette troisième étape consiste à créer de la valeur à partir des données brutes via un pipeline NLP complet.

```mermaid
graph TD
    A[① Extraction MongoDB<br/>66k avis bruts] --> B[② Annotation BERT<br/>Sentiment + Notes 1-5]
    B --> C[③ Nettoyage<br/>Doublons + Outliers]
    C --> D[④ Préprocessing NLP<br/>Lemmatisation + Négations]
    D --> E[⑤ Benchmarking ML<br/>3 modèles testés]
    E --> F[⑥ Sélection LinearSVC<br/>Meilleur F1-score]
    F --> G[⑦ Suivi MLflow<br/>Versioning + Métriques]
    G --> H[⑧ Déploiement<br/>API + Streamlit]
    
    style A fill:#e3f2fd
    style B fill:#f3e5f5
    style C fill:#e8f5e9
    style D fill:#fff9c4
    style E fill:#ffecb3
    style F fill:#c8e6c9
    style G fill:#b3e5fc
    style H fill:#f8bbd0
```

### 📋 Pipeline de Traitement (8 Étapes)

| Étape | Objectif | Détails |
|-------|----------|---------|
| **① Extraction** | Consolidation des données | Export des avis bruts depuis MongoDB |
| **② Annotation BERT** | Génération des labels | Utilisation de BERT pour sentiment et note (1–5) |
| **③ Nettoyage** | Amélioration de la qualité | Suppression doublons, outliers, commentaires non exploitables |
| **④ Preprocessing NLP** | Préparation linguistique | Lemmatisation, gestion des négations, normalisation |
| **⑤ Benchmarking** | Comparaison de modèles | Entraînement et évaluation de 3 modèles supervisés |
| **⑥ Sélection** | Choix du meilleur modèle | LinearSVC retenu et sérialisation effectuée |
| **⑦ Suivi MLflow** | Traçabilité complète | Suivi des runs, métriques, versioning des modèles |
| **⑧ Déploiement** | Exposition des résultats | Streamlit, dashboards MLflow, visualisations |

### 📊 Benchmarking et Sélection du Modèle

Une évaluation comparative a été menée sur **trois modèles** pour identifier le plus performant sur les tâches d'analyse de sentiment et de prédiction de note. Les performances sont mesurées sur un jeu de test de **20%** des données.

#### Résultats Détaillés

| Tâche | Modèle | Accuracy | F1-score (macro) | 🏆 |
|-------|--------|----------|------------------|-----|
| **Sentiment** | LogisticRegression | 82.62% | 0.7537 | |
| **Sentiment** | **LinearSVC** | **85.06%** | **0.7546** | ✅ |
| **Sentiment** | RandomForest | 81.40% | 0.6445 | |
| **Note** | LogisticRegression | 70.73% | 0.4697 | |
| **Note** | **LinearSVC** | **80.43%** | **0.4949** | ✅ |
| **Note** | RandomForest | 79.48% | 0.3594 | |

```mermaid
graph LR
    A[LinearSVC] -->|Sentiment: 85.06%| B[Meilleur Accuracy]
    A -->|Note: 80.43%| C[Meilleur F1-score]
    A -->|Performance équilibrée| D[Modèle Retenu]
    
    style A fill:#4caf50,color:#fff
    style D fill:#2196f3,color:#fff
```

**🎯 Modèle Retenu :** **LinearSVC** obtient les meilleurs scores d'Accuracy et de F1-score sur les deux tâches. Il démontre une capacité supérieure à gérer les classes déséquilibrées. Il a donc été privilégié pour l'intégration dans l'API.

---

## 🚀 Partie 4 : API & Déploiement Docker

Cette quatrième étape consiste à exposer les modèles et les données via une API sécurisée et conteneurisée.

```mermaid
graph TB
    subgraph Utilisateurs
        A[Client Web]
        B[Dashboard Streamlit]
    end
    
    subgraph API Layer
        C[FastAPI<br/>Endpoints REST]
        D[JWT Auth<br/>3 Modes]
    end
    
    subgraph Services
        E[MongoDB<br/>Avis]
        F[PostgreSQL<br/>Métadonnées]
        G[ML Models<br/>LinearSVC]
    end
    
    subgraph Infrastructure
        H[Docker<br/>17 Conteneurs]
        I[Tests Pytest<br/>78% Coverage]
    end
    
    A --> C
    B --> C
    C --> D
    D --> E
    D --> F
    D --> G
    C --> H
    H --> I
    
    style C fill:#00bcd4,color:#fff
    style H fill:#ff9800,color:#fff
    style D fill:#4caf50,color:#fff
```

### 🔑 Composants Clés de l'Architecture

| Composant | Quantité | Description |
|-----------|----------|-------------|
| **API FastAPI** | 1 | Expose des endpoints REST pour consulter, prédire et exporter les avis |
| **Conteneurs Docker** | 17 | Isolent chaque service pour un déploiement cohérent et scalable |
| **Tests Pytest** | 17 tests | Garantit la robustesse de l'API avec une couverture de **78%** |
| **Sécurité JWT** | 3 modes | Authentification flexible : Off, Partial, Full |
| **Interfaces Streamlit** | 2 | Dashboard analytique + Testeur ML (note et sentiment) |

### 📡 Endpoints API Principaux

```python
# Exemple d'utilisation de l'API
import requests

# Authentification JWT
response = requests.post("http://localhost:8000/token", 
                         data={"username": "user", "password": "pass"})
token = response.json()["access_token"]

# Prédiction de sentiment
headers = {"Authorization": f"Bearer {token}"}
data = {"text": "Produit excellent mais livraison tardive"}
response = requests.post("http://localhost:8000/predict/sentiment", 
                         json=data, headers=headers)
print(response.json())
# Output: {"sentiment": "mixte", "confidence": 0.73, "note_predite": 3}
```

### 🔐 Modes d'Authentification JWT

- **Off** : Aucune authentification (développement)
- **Partial** : Authentification sur endpoints sensibles uniquement
- **Full** : Authentification requise sur tous les endpoints (production)

---

## 🔧 Partie 5 : MLOps & Industrialisation

Cette cinquième étape consiste à industrialiser le projet via une approche MLOps complète.

```mermaid
graph TB
    subgraph Orchestration
        A[Apache Airflow<br/>DAGs Automatisés]
        B[Scraping Quotidien]
        C[Preprocessing]
        D[ML Training]
    end
    
    subgraph CI/CD
        E[GitLab Runner<br/>Local]
        F[Linting flake8]
        G[Tests API Docker]
        H[Non-régression]
    end
    
    subgraph Monitoring
        I[Prometheus<br/>Collecte Métriques]
        J[Grafana<br/>Dashboards]
        K[Alertes Temps Réel]
    end
    
    A --> B
    A --> C
    A --> D
    E --> F
    F --> G
    G --> H
    I --> J
    J --> K
    
    style A fill:#ff6f00,color:#fff
    style E fill:#fc4c02,color:#fff
    style I fill:#e91e63,color:#fff
```

### ⚙️ Composants MLOps

#### 🔄 Orchestration avec Apache Airflow

- **DAGs distincts** pour chaque pipeline : scraping, insertion, preprocessing, ML
- **Mode d'exécution manuel** pour tester et relancer à la demande
- Pilote le pipeline complet de bout en bout
- Gestion des dépendances et des échecs avec retry automatique

#### 🔁 CI/CD avec GitLab

- **Shell Runner local** pour l'exécution des pipelines
- **Pipeline automatisé** incluant :
  - Linting avec **flake8** (vérification qualité code)
  - Tests de l'API FastAPI dans son **conteneur Docker**
  - Garantit la **non-régression** à chaque commit
- Déploiement automatique des images Docker après validation

#### 📊 Supervision avec Prometheus & Grafana

- **Prometheus** : Collecte des métriques des services, conteneurs et système
  - CPU, mémoire, réseau, latence
  - Métriques métier (nombre de prédictions, erreurs, etc.)
- **Grafana** : Centralise les informations dans des dashboards visuels
  - Suivi en temps réel de la plateforme
  - Alertes configurables (Slack, Email)
  - Analyse des tendances et anomalies

---

## 📊 Résultats Métier

L'analyse des sentiments et des thèmes abordés dans les avis permettent de formuler un **diagnostic et des recommandations actionnables** pour chaque entreprise.

### 📈 Synthèse par Entreprise

```mermaid
mindmap
  root((Insights Métier))
    Tesla
      ✅ Innovation Produit
      ❌ Service Après-Vente
      💡 Expérience Post-Achat
    Chronopost
      ✅ Rapidité Réseau
      ❌ Flexibilité Dernier Km
      💡 Suivi Temps Réel
    Vinted
      ✅ Communauté Active
      ❌ Lenteur Arbitrage
      💡 Médiation Rapide
    Temu
      ✅ Prix Attractifs
      ❌ Écart Attentes/Réalité
      💡 Gestion Attentes
```

### 🎯 Tableau de Diagnostic Complet

| Entreprise | 💪 Pilier (Point Fort) | 😣 Douleur (Point Faible) | 💡 Recommandations |
|------------|----------------------|---------------------------|-------------------|
| **Tesla** | Innovation Produit | Service Après-Vente | Investir dans l'**expérience post-achat** pour protéger l'image premium |
| **Chronopost** | Rapidité du réseau | Manque de flexibilité du dernier kilomètre | Améliorer le **suivi en temps réel** et les solutions de recours |
| **Vinted** | Force de la communauté | Lenteur et injustice perçue dans l'arbitrage des litiges | Renforcer la confiance via une **médiation plus juste et rapide** |
| **Temu** | Prix bas | Écart entre les attentes (photos) et la réalité (qualité, délais) | **Gérer les attentes** et simplifier les retours |

### 🔍 Insights Clés Transversaux

- **📈 Polarisation marquée** : 75% des avis sont 1/5 ou 5/5 (très peu de notes intermédiaires)
- **🔍 Thèmes récurrents** : 
  - Livraison (35%)
  - Service client (28%)
  - Qualité produit (22%)
  - Prix/rapport qualité-prix (15%)
- **🎯 Mots influents identifiés** :
  - ✅ **Positifs** : excellent, parfait, rapide, top, efficace, professionnel
  - ❌ **Négatifs** : problème, attente, déçu, lent, cassé, arnaque

---

## ⚙️ Guide d'Installation

### Prérequis

```bash
# Vérifier les versions installées
python --version        # >= 3.9 requis
docker --version        # >= 20.10 requis
docker-compose version  # >= 2.0 requis
```

### Installation Complète

```bash
# 1. Clone du repository
git clone https://github.com/Didier2024-hue/trustpilot-analysis.git
cd trustpilot-analysis

# 2. Configuration de l'environnement
cp .env.example .env
nano .env  # Éditer avec vos configurations

# 3. Installation des dépendances Python
pip install -r requirements.txt

# 4. Lancement des services Docker (17 conteneurs)
docker-compose up -d --build

# 5. Initialisation des bases de données
python scripts/scraping/creation_mongodb.py
python scripts/scraping/creation_postgre.py

# 6. Collecte initiale des données
python scripts/scraping/cde_scrap_new.py      # Trustpilot
python scripts/scraping/cde_scrap_wiki.py     # Wikipedia

# 7. Pipeline Machine Learning
python scripts/ml/snapshot_data.py            # Export données
python scripts/ml/sentiment_analysis.py       # Annotation BERT
python scripts/ml/clean_data.py               # Nettoyage
python scripts/ml/preprocessing_demo_ml.py    # Preprocessing NLP
python scripts/ml/train_dual_models.py        # Entraînement modèles

# 8. Démarrage de l'API
python scripts/api/main.py
```

### 🌐 Accès aux Services

| Service | URL | Port | Identifiants | Description |
|---------|-----|------|--------------|-------------|
| **FastAPI** | http://localhost:8000 | 8000 | - | API principale + documentation Swagger |
| **Streamlit Dashboard** | http://localhost:8501 | 8501 | - | Dashboard analytique interactif |
| **Streamlit Tester** | http://localhost:8502 | 8502 | - | Testeur ML (sentiment + note) |
| **MLflow** | http://localhost:5000 | 5000 | - | Tracking expérimentations ML |
| **Airflow** | http://localhost:8080 | 8080 | admin/admin | Orchestration workflows |
| **Grafana** | http://localhost:3000 | 3000 | admin/admin | Monitoring temps réel |
| **Prometheus** | http://localhost:9090 | 9090 | - | Collecte métriques système |

### 🔧 Configuration Avancée

```bash
# Variables d'environnement (.env)
MONGODB_URI=mongodb://localhost:27017
POSTGRES_URI=postgresql://user:pass@localhost:5432/trustpilot
JWT_SECRET_KEY=your-secret-key-here
JWT_MODE=full  # off, partial, full
MLFLOW_TRACKING_URI=http://localhost:5000
```

---

## 📁 Structure du Projet

```
trustpilot-analysis/
├── 📂 scripts/
│   ├── 📂 scraping/
│   │   ├── cde_scrap_new.py          # Scraping Trustpilot quotidien
│   │   ├── cde_scrap_wiki.py         # Collecte Wikipedia mensuelle
│   │   ├── creation_mongodb.py       # Init MongoDB
│   │   └── creation_postgre.py       # Init PostgreSQL
│   ├── 📂 ml/
│   │   ├── snapshot_data.py          # Export MongoDB → CSV
│   │   ├── sentiment_analysis.py     # Annotation BERT
│   │   ├── clean_data.py             # Nettoyage données
│   │   ├── preprocessing_demo_ml.py  # Preprocessing NLP
│   │   ├── train_dual_models.py      # Benchmarking modèles
│   │   ├── save_model.py             # Sérialisation modèles
│   │   └── mlflow_tracking.py        # Suivi expérimentations
│   └── 📂 api/
│       ├── main.py                   # API FastAPI principale
│       ├── auth.py                   # Authentification JWT
│       ├── endpoints/                # Endpoints REST
│       └── tests/                    # Tests Pytest (78% coverage)
├── 📂 dashboard/
│   ├── app_streamlit.py              # Dashboard analytique
│   └── tester_ml.py                  # Interface testeur ML
├── 📂 mlops/
│   ├── 📂 dags/                      # DAGs Airflow
│   │   ├── dag_scraping.py
│   │   ├── dag_preprocessing.py
│   │   └── dag_training.py
│   ├── .gitlab-ci.yml                # Pipeline CI/CD
│   └── 📂 monitoring/
│       ├── prometheus.yml            # Config Prometheus
│       └── grafana_dashboards/       # Dashboards Grafana
├── 📂 docker/
│   ├── Dockerfile.api                # Image FastAPI
│   ├── Dockerfile.streamlit          # Image Streamlit
│   ├── Dockerfile.mlflow             # Image MLflow
│   ├── Dockerfile.airflow            # Image Airflow
│   └── docker-compose.yml            # Orchestration 17 conteneurs
├── 📂 data/
│   ├── 📂 raw/                       # Données brutes collectées
│   ├── 📂 processed/                 # Données nettoyées
│   └── 📂 models/                    # Modèles ML sérialisés
├── 📂 notebooks/
│   ├── analysis.ipynb                # Analyses exploratoires
│   └── visualization.ipynb           # Visualisations graphiques
├── 📂 docs/
│   ├── architecture.md               # Documentation architecture
│   ├── api_documentation.md          # Documentation API
│   └── mlops_guide.md                # Guide MLOps
├── requirements.txt                   # Dépendances Python
├── docker-compose.yml                 # Orchestration services
├── .env.example                       # Template configuration
├── .gitignore                         # Fichiers ignorés Git
├── LICENSE                            # Licence MIT
└── README.md                          # Ce fichier
```

---

## 👥 Équipe

<div align="center">

| Rôle | Nom | Contribution |
|------|-----|--------------|
| **🎓 Auteur** | **Didier Joséphine** | Développement complet du projet end-to-end |
| **👨‍🏫 Tuteur** | **Rémy D.** | Encadrement technique et méthodologique |
| **💼 COO** | **Vincent L.** | Supervision métier et stratégique |
| **🏢 Organisme** | **Liora (ex : DataScientest) ** | Formation Data Engineer - Promotion 2025 |

</div>

### 📧 Contact & Liens

- **Email** : kiembraid@gmail.com
- **GitHub** : [@Didier2024-hue](https://github.com/Didier2024-hue)
- **Formation** : Data Engineer - Promotion 2025
- **Spécialité** : Supply Chain & Satisfaction Client

---

## 📄 Licence

<div align="center">

**Projet Académique - Formation Data Engineer**

Ce projet est un travail académique réalisé dans le cadre de la formation Data Engineer de DataScientest.

Distribué sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

⚠️ **Note Importante** : Les données Trustpilot sont utilisées à des fins **éducatives uniquement** et respectent les conditions d'utilisation du site.

---

**Dernière mise à jour** : Mars 2026  
**Statut du projet** : ✅ **Production - MLOps Industrialisé**

---

<sub>DataScientest • Data Engineer • Promotion 2025</sub>

</div>
