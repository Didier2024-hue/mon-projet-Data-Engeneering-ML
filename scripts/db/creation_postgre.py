import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# Charger automatiquement le fichier .env depuis le dossier courant
load_dotenv()

# Récupérer les variables d'environnement pour les chemins
BASE_DIR = os.getenv("BASE_DIR")
LOG_DIR = os.getenv("LOG_DIR")

def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def get_log_file():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(LOG_DIR, f"create_tables_{now}.log")

class Logger:
    def __init__(self, filepath):
        self.filepath = filepath
        self.log_lines = []

    def print(self, msg):
        print(msg)
        self.log_lines.append(msg)

    def save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(self.log_lines))

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

def create_tables(cur, log):
    log.print("🔄 Suppression des tables existantes si elles existent...")

    cur.execute("DROP TABLE IF EXISTS avis_trustpilot;")
    cur.execute("DROP TABLE IF EXISTS societe;")
    log.print("✅ Tables supprimées (si elles existaient).")

    log.print("🔄 Création de la table societe...")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS societe (
        id_societe SERIAL PRIMARY KEY,
        nom VARCHAR(255) UNIQUE NOT NULL,
        url TEXT,
        secteur VARCHAR(255),
        note_globale REAL,
        nombre_avis INTEGER,
        note_1 INTEGER,
        note_2 INTEGER,
        note_3 INTEGER,
        note_4 INTEGER,
        note_5 INTEGER,
        date_extraction TIMESTAMP,
        nombre_commentaires INTEGER
    );
    """)
    log.print("✅ Table societe créée.")

    log.print("🔄 Création de la table avis_trustpilot...")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS avis_trustpilot (
        id_avis SERIAL PRIMARY KEY,
        id_societe INTEGER REFERENCES societe(id_societe),
        page INTEGER,
        url_page TEXT,
        auteur VARCHAR(255),
        date_avis TIMESTAMP,
        commentaire TEXT,
        note_commentaire INTEGER,
        date_chargement TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)
    log.print("✅ Table avis_trustpilot créée.")

def main():
    ensure_log_dir()
    log = Logger(get_log_file())

    try:
        conn = connect_db()
        cur = conn.cursor()

        log.print("🚀 Connexion à la base PostgreSQL réussie.")
        create_tables(cur, log)

        conn.commit()
        log.print("🎉 Commit effectué, tables créées avec succès.")

        cur.close()
        conn.close()
        log.print("🔌 Connexion fermée proprement.")

    except Exception as e:
        log.print(f"❌ ERREUR lors de la création des tables : {e}")

    log.save()
    log.print(f"📁 Log sauvegardé dans : {log.filepath}")

if __name__ == "__main__":
    main()
