import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from pprint import pformat

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGO_URI = (
    f"mongodb://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}"
    f"@{os.getenv('MONGO_HOST')}:{os.getenv('MONGO_PORT')}/"
)

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler()]
)

def print_separator(title=None, width=60):
    """Affiche une ligne de séparation avec titre optionnel"""
    if title:
        logging.info("\n" + "=" * width)
        logging.info(f" {title.upper()} ".center(width, '='))
        logging.info("=" * width + "\n")
    else:
        logging.info("-" * width)

def print_document(doc, doc_num, width=60):
    """Affiche un document de manière formatée"""
    logging.info(f"\n📄 DOCUMENT #{doc_num}")
    logging.info("-" * width)
    formatted_doc = pformat(doc, width=width, indent=2, depth=2)
    for line in formatted_doc.split('\n'):
        logging.info(line)
    logging.info("-" * width)

def print_database_info(client, sample_size=5):
    """Affiche les bases, collections et exemples de documents"""
    print_separator("Structure MongoDB")
    for db_name in sorted(client.list_database_names()):
        if db_name not in ['admin', 'config', 'local']:
            db = client[db_name]
            logging.info(f"\n🗂 BASE DE DONNÉES: {db_name}")
            for col_name in sorted(db.list_collection_names()):
                print_separator(f"Collection: {col_name}")
                stats = db.command("collstats", col_name)
                logging.info(f"Documents totaux: {stats['count']:,}")
                logging.info(f"Taille: {stats['size']/(1024*1024):.2f} MB\n")
                try:
                    for i, doc in enumerate(db[col_name].find().limit(sample_size), 1):
                        print_document(doc, i)
                except Exception as e:
                    logging.error(f"Erreur lecture documents: {str(e)}")

def main():
    try:
        client = MongoClient(MONGO_URI)
        print_database_info(client)
    except Exception as e:
        logging.error(f"Erreur connexion: {str(e)}")
    finally:
        if 'client' in locals():
            client.close()
            logging.info("Connexion MongoDB fermée")

if __name__ == "__main__":
    main()
