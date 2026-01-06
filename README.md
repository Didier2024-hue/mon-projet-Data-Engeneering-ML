# 🟩🟨🟥 Analyse de la Satisfaction Client – Trustpilot 🟥🟨🟩

Projet réalisé dans le cadre de la formation **Data Engineer – DataScientest (Promotion 2025, Supply Chain & Satisfaction Client)**.  
Ce projet met en œuvre une approche **end-to-end** d’analyse de la satisfaction client à partir d’avis **Trustpilot**, depuis la collecte automatisée des données jusqu’à leur exposition via une **API sécurisée**, en intégrant des pratiques **Data Engineering, Machine Learning et MLOps**.

---

## 🔎 Résumé exécutif

- 🔎 **Collecte automatisée** de plus de **66 000 avis Trustpilot** et de données sociétales issues de Wikipédia  
- 🗃️ **Architecture bi-base** : MongoDB (avis clients) et PostgreSQL (métadonnées entreprises)  
- 🤖 **Pipeline NLP & ML complet** avec annotation BERT et modèles supervisés (TF-IDF + SVM)  
- 🚀 **API FastAPI sécurisée (JWT)**, conteneurisée avec Docker et testée à 78 %  
- 🔧 **Industrialisation MLOps** : Airflow, GitLab CI/CD, Prometheus & Grafana  

Objectif : fournir une **plateforme industrialisée de veille concurrentielle** et d’aide à la décision basée sur l’analyse des sentiments clients.

---

## 🏢 Périmètre du projet

L’analyse se concentre sur quatre entreprises représentatives de secteurs variés afin de permettre une comparaison intersectorielle.

| Entreprise | Secteur | Enjeux principaux |
|----------|--------|-------------------|
| **Tesla** | Automobile / Énergie verte | Innovation, qualité produit, service après-vente |
| **Temu** | E-commerce B2C | Rapport qualité-prix, délais, satisfaction |
| **Chronopost** | Logistique | Ponctualité, gestion des réclamations |
| **Vinted** | Marketplace C2C | Expérience utilisateur, confiance |

---

## 🏗️ Architecture fonctionnelle globale

Le projet suit une architecture **end-to-end**, couvrant l’ensemble du cycle de vie de la donnée.

1. **Collecte**  
   - Scraping automatisé des avis Trustpilot  
   - Collecte des données entreprises via l’API Wikipédia  

2. **Stockage**  
   - MongoDB : avis clients bruts (format JSON, schemaless)  
   - PostgreSQL : métadonnées structurées (schéma relationnel normalisé)  

3. **Préparation & NLP**  
   - Nettoyage, normalisation et enrichissement sémantique  
   - Annotation automatique des sentiments et notes via BERT  

4. **Modélisation**  
   - Entraînement et benchmarking de modèles supervisés  
   - Suivi des expérimentations avec MLflow  

5. **Exposition**  
   - API FastAPI sécurisée par JWT  
   - Interfaces Streamlit pour visualisation et tests  

6. **MLOps**  
   - Orchestration Airflow  
   - CI/CD GitLab  
   - Monitoring Prometheus & Grafana  

---

## 🔎 Collecte des données

### Avis clients – Trustpilot
- Scraping automatisé quotidien
- Collecte historisée et horodatée
- Stockage brut dans MongoDB
- Processus résilient (reprise sur incident, respect robots.txt)

### Données entreprises – Wikipédia
- Collecte mensuelle via API
- Enrichissement métier (CA, secteur, SIREN, fondateur…)
- Stockage structuré dans PostgreSQL

---

## 🗃️ Stockage des données

### PostgreSQL
- Métadonnées entreprises
- Schéma relationnel normalisé
- Backend MLflow pour le suivi des modèles

### MongoDB
- Avis Trustpilot au format JSON
- Flexibilité documentaire
- Optimisé pour gros volumes et accès rapides

---

## 🤖 Machine Learning & NLP

### Pipeline ML
1. Extraction des avis depuis MongoDB  
2. Annotation automatique des labels (sentiment & note 1–5) via BERT  
3. Nettoyage (doublons, outliers, commentaires non exploitables)  
4. Prétraitement NLP avancé (lemmatisation, négations, normalisation)  
5. Vectorisation TF-IDF  
6. Entraînement et benchmarking multi-modèles  
7. Sélection, sérialisation et versioning  
8. Suivi expérimental avec MLflow  

### Résultats du benchmarking

| Tâche | Modèle | Accuracy | F1-score (macro) |
|-----|-------|----------|------------------|
| Sentiment | Logistic Regression | 82.62 % | 0.7537 |
| Sentiment | **LinearSVC** | **85.06 %** | **0.7546** |
| Sentiment | Random Forest | 81.40 % | 0.6445 |
| Note | Logistic Regression | 70.73 % | 0.4697 |
| Note | **LinearSVC** | **80.43 %** | **0.4949** |
| Note | Random Forest | 79.48 % | 0.3594 |

➡️ **Modèle retenu : LinearSVC**

---

## 🚀 API & Déploiement

- **FastAPI** : endpoints REST (consultation, prédiction, export)  
- **Sécurité** : authentification JWT (Off / Partial / Full)  
- **Docker** : 17 conteneurs isolés  
- **Tests** : Pytest, 78 % de couverture  
- **Streamlit** : dashboards métier et interface de test ML  

---

## 🔧 MLOps & Supervision

- **Airflow** : orchestration complète du pipeline (scraping → ML → déploiement)  
- **GitLab CI/CD** : linting, tests automatisés et validation Docker  
- **Prometheus** : collecte des métriques système et applicatives  
- **Grafana** : dashboards temps réel et supervision continue  

---

## 📊 Résumé métier

| Entreprise | Point fort | Point faible | Recommandation |
|----------|-----------|-------------|----------------|
| Tesla | Innovation produit | Service après-vente | Renforcer l’expérience post-achat |
| Chronopost | Rapidité réseau | Dernier kilomètre | Améliorer le suivi temps réel |
| Vinted | Communauté | Gestion des litiges | Médiation plus rapide et juste |
| Temu | Prix bas | Attentes vs réalité | Clarifier l’offre et les retours |

---

## 👤 Auteur

**Didier J.**  
Formation **Data Engineer – DataScientest**  
📧 Email : kiembraid@gmail.com  
🔗 GitHub : Didier2024-hue  

---

## 📄 Licence

Projet académique distribué sous licence **MIT**.  
Voir le fichier `LICENSE` pour plus de détails.
