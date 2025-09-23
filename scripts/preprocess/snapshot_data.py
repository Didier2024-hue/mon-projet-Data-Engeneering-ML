import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
from datetime import datetime

# Chargement des variables d'environnement
load_dotenv()

# Variables d'environnement requises
REQUIRED_ENV_VARS = ['DATA_EXPORTS', 'MONGO_URI', 'LOG_DIR']
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
if missing_vars:
    print(f"\n❌ ERREUR : Variables manquantes dans .env : {', '.join(missing_vars)}")
    raise EnvironmentError("Configuration manquante")

EXPORT_DIR = os.getenv('DATA_EXPORTS')
MONGO_URI = os.getenv('MONGO_URI')
MONGO_DB = os.getenv('MONGO_DB') or 'trustpilot'
LOG_DIR = os.getenv('LOG_DIR')
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')

# Initialisation du logger
log_filename = os.path.join(LOG_DIR, f"export_mongo_trustpilot_avis_{TIMESTAMP}.log")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def verify_export_dir():
    """Vérifie que le répertoire d'export est accessible"""
    logging.info(f"Vérification du répertoire d'export : {EXPORT_DIR}")
    if not os.path.isdir(EXPORT_DIR):
        raise NotADirectoryError(f"Le répertoire {EXPORT_DIR} n'existe pas")
    try:
        test_file = os.path.join(EXPORT_DIR, 'test.tmp')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        logging.info("✓ Répertoire d'export valide")
    except Exception as e:
        raise PermissionError(f"Impossible d'écrire dans {EXPORT_DIR} : {e}")

def init_mongo_client():
    """Connexion MongoDB"""
    logging.info(f"Connexion à MongoDB...")
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')
        logging.info("✓ Connexion MongoDB réussie")
        return client
    except Exception as e:
        raise ConnectionError(f"Erreur de connexion MongoDB : {e}")

def export_trustpilot_collections(client):
    """Exporte les collections avis_trustpilot et societe"""
    logging.info("Export des collections depuis la base 'trustpilot'")
    db = client[MONGO_DB]
    target_collections = ['avis_trustpilot', 'societe']

    for col_name in target_collections:
        logging.info(f"→ Export de la collection : {col_name}")
        try:
            docs = list(db[col_name].find({}, {'_id': 0}))
            if not docs:
                logging.warning(f"Collection {col_name} vide – ignorée")
                continue

            filename = f"mongo_trustpilot_{col_name}.csv"
            filepath = os.path.join(EXPORT_DIR, filename)
            df = pd.DataFrame(docs)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')

            logging.info(f"   ✓ {len(df)} lignes exportées")
            logging.info(f"   📄 Fichier généré : {filename}")
        except Exception as e:
            logging.error(f"   ❌ Erreur lors de l'export de {col_name} : {e}")

def main():
    print("\n" + "="*50)
    print("  EXPORT MONGODB TRUSTPILOT AVIS")
    print("="*50)

    client = None
    try:
        verify_export_dir()
        client = init_mongo_client()
        export_trustpilot_collections(client)
        logging.info("✅ Export terminé avec succès.")
    except Exception as e:
        logging.error(f"❌ ERREUR : Le processus a échoué : {e}")
    finally:
        if client:
            client.close()
            logging.info("🔌 Connexion MongoDB fermée.")

if __name__ == "__main__":
    main()
