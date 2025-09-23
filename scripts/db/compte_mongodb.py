import os
import logging
import time
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING

# 🔧 Chargement des variables d'environnement
load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_DB = os.getenv('MONGO_DB')

MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

# 🗂️ Configuration des logs
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'mongodb_import.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def banner(text):
    sep = '*' * 70
    return f"\n{sep}\n*** {text}\n{sep}\n"

def create_indexes(db):
    try:
        logging.info("📌 Création des index...")
        db.societe.create_index([('nom', ASCENDING)], unique=True)
        db.avis_trustpilot.create_index([('nom_societe', ASCENDING)])
        logging.info("✅ Index créés avec succès.")
    except Exception as e:
        logging.error(f"❌ Erreur création index : {str(e)}")

def get_collection_stats(db, collection_name):
    return {
        'count': db[collection_name].estimated_document_count(),
        'size': db.command('collstats', collection_name).get('size', 0)
    }

def display_collection_preview(db, collection_name, limit=5):
    try:
        stats = get_collection_stats(db, collection_name)

        logging.info(banner(
            f"📊 Aperçu de la collection: {collection_name}\n"
            f"📄 Documents: {stats['count']:,} | 💾 Taille: {stats['size']:,} octets"
        ))

        cursor = db[collection_name].find().limit(limit)
        for i, doc in enumerate(cursor, 1):
            logging.info(f"🔎 Document {i}: {doc}")

        if stats['count'] == 0:
            logging.warning("⚠️ Aucun document trouvé.")

    except Exception as e:
        logging.error(f"❌ Erreur accès collection {collection_name}: {str(e)}")
    
    time.sleep(1)

def main():
    try:
        logging.info(banner("🚀 Connexion à MongoDB"))
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=3000
        )

        client.admin.command('ping')
        db = client[MONGO_DB]
        logging.info(f"✅ Connexion réussie à la base : {MONGO_DB}")

        logging.info(banner("🔧 Création des index"))
        create_indexes(db)

        logging.info(banner("📈 Statistiques des collections"))
        for col in db.list_collection_names():
            stats = get_collection_stats(db, col)
            logging.info(
                f"{col.ljust(20)}: {str(stats['count']).rjust(8)} documents | "
                f"{str(round(stats['size'] / (1024 * 1024), 2)).rjust(6)} MB"
            )

        for col in ['societe', 'avis_trustpilot']:
            if col in db.list_collection_names():
                display_collection_preview(db, col)
                logging.info("\n" + "="*70 + "\n")
                time.sleep(1)

    except Exception as e:
        logging.critical(f"❌ ERREUR critique : {str(e)}")
    finally:
        if 'client' in locals():
            client.close()
            logging.info(banner("🔒 Connexion fermée proprement"))

if __name__ == "__main__":
    main()
