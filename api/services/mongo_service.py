# services/mongo_service.py
import os
import re
import logging
import time
from pymongo import MongoClient
from dotenv import load_dotenv

# -----------------------
# Charger le .env.api
# -----------------------
BASE_DIR = os.getenv("BASE_DIR") or os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
dotenv_path = os.path.join(BASE_DIR, ".env.api")
load_dotenv("/home/datascientest/cde/api/.env.api")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# -----------------------
# Configuration MongoDB
# -----------------------
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

if not MONGO_URI or not MONGO_DB:
    raise EnvironmentError("MONGO_URI et MONGO_DB doivent être définis dans .env.api")

def get_mongo_collection():
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db[MONGO_COLLECTION]

# -----------------------
# Connexion MongoDB avec retry
# -----------------------
def get_mongo_db(uri, db_name, max_retries=5, retry_delay=3):
    for attempt in range(max_retries):
        try:
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            db = client[db_name]
            logging.info("✅ Connected to MongoDB (db=%s)", db_name)
            return client, db
        except Exception as e:
            logging.warning("MongoDB not ready, retry %d/%d: %s", attempt+1, max_retries, e)
            time.sleep(retry_delay)
    raise ConnectionError(f"❌ Cannot connect to MongoDB at {uri} after {max_retries} attempts")

client, db = get_mongo_db(MONGO_URI, MONGO_DB)

# Collections utilisées
collection_avis = db["avis_trustpilot"]
collection_societes = db["societe"]

# -----------------------
# Helpers
# -----------------------
def _build_regex_pattern(s: str):
    if not s:
        return None
    return {"$regex": re.escape(s.strip()), "$options": "i"}

# -----------------------
# Récupération des derniers commentaires
# -----------------------
def get_last_comments(societe_id: str = None, limit: int = 100, skip: int = 0):
    limit = int(limit) if limit else 100
    skip = int(skip) if skip else 0

    query = {}
    if societe_id:
        pat = _build_regex_pattern(societe_id)
        query = {
            "$or": [
                {"id_societe": pat},
                {"societe_nom": pat},
                {"societe": pat},
                {"nom": pat},
                {"url_page": pat}
            ]
        }

    cursor = collection_avis.find(query).sort("date_chargement", -1).skip(skip).limit(limit)
    return [{**d, "_id": str(d["_id"])} for d in cursor]

# -----------------------
# Liste des sociétés avec note globale + total avis
# -----------------------
def list_societes(limit: int = 1000):
    cursor = collection_societes.find(
        {},
        {"_id": 0, "nom": 1, "note_globale": 1, "total_avis": 1}
    ).limit(limit)

    res = list(cursor)

    # Ajouter un identifiant lisible basé sur le nom
    for r in res:
        r["id"] = r["nom"].split(".")[0] if "nom" in r else ""
        r["total_avis"] = int(r.get("total_avis", 0))
    return res

# -----------------------
# Top Avis
# -----------------------
def get_top_avis(societe_id: str, limit: int = 10, positif: bool = True):
    query = {"id_societe": {"$regex": societe_id, "$options": "i"}}
    sort_order = -1 if positif else 1  # meilleurs avis = plus grande note
    cursor = collection_avis.find(query).sort("note", sort_order).limit(limit)
    return [{**d, "_id": str(d["_id"])} for d in cursor]
