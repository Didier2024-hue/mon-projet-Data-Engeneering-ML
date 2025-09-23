import os
import psycopg2
import json
import re
from datetime import datetime
from dotenv import load_dotenv

# Initialisation environnement
load_dotenv()

# Configuration via variables d'environnement
BASE_DIR = os.environ['BASE_DIR']
DATA_SUBDIR = os.environ.get('WIKI_DATA_DIR', 'data/wikipedia')
LOG_SUBDIR = os.environ.get('LOG_DIR', 'log')

# Chemins complets
DATA_DIR = os.path.join(BASE_DIR, DATA_SUBDIR)
LOG_DIR = os.path.join(BASE_DIR, LOG_SUBDIR)

# Fichiers à traiter
COMPANY_FILES = {
    'temu': '1_infobox.json',
    'tesla': '2_infobox.json',
    'chronopost': '3_infobox.json',
    'vinted': '4_infobox.json'
}

def get_db_conn():
    """Connexion PostgreSQL"""
    return psycopg2.connect(
        dbname=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        host=os.environ['POSTGRES_HOST'],
        port=os.environ['POSTGRES_PORT']
    )

def safe_name(name):
    """Normalisation des noms SQL"""
    return re.sub(r'[^a-z0-9]', '_', str(name).lower()).strip('_')

def log_step(message, log_file=None):
    """Journalisation avec affichage console"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    output = f"[{timestamp}] {message}"
    print(output)
    if log_file:
        log_file.write(output + '\n')

def process_company(conn, log_file, company, filename):
    """Traitement complet d'une entreprise"""
    try:
        filepath = os.path.join(DATA_DIR, filename)
        
        # Vérification fichier
        if not os.path.exists(filepath):
            log_step(f"ERREUR: Fichier {filename} introuvable pour {company}", log_file)
            return False

        log_step(f"Début traitement {company}...", log_file)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with conn.cursor() as cur:
            # Création table
            table_name = f"wiki_{safe_name(company)}"
            log_step(f"Création table {table_name}...", log_file)
            
            columns = ['id SERIAL PRIMARY KEY']
            values = []
            placeholders = []
            
            for key, val in data.items():
                col_name = safe_name(key)
                col_type = 'TEXT'
                
                if isinstance(val, (int, float)):
                    col_type = 'NUMERIC' if isinstance(val, float) else 'INTEGER'
                columns.append(f"{col_name} {col_type}")
                values.append(val)
                placeholders.append('%s')

            # Exécution SQL
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            cur.execute(f"CREATE TABLE {table_name} ({', '.join(columns)})")
            log_step(f"Structure créée avec {len(columns)} colonnes", log_file)
            
            # Insertion données
            cur.execute(
                f"INSERT INTO {table_name} ({', '.join(safe_name(k) for k in data.keys())}) VALUES ({', '.join(placeholders)})",
                values
            )
            
            # Vérification
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cur.fetchone()[0]
            log_step(f"Données chargées: {count} enregistrement(s)", log_file)
            
            log_step(f"SUCCÈS: Table {table_name} prête", log_file)
            return True

    except Exception as e:
        log_step(f"ÉCHEC: {str(e)}", log_file)
        return False

def main():
    """Exécution principale"""
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"import_wiki_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    
    with open(log_path, 'w', encoding='utf-8') as log_file:
        log_step("=== DÉBUT IMPORTATION ===", log_file)
        
        try:
            with get_db_conn() as conn:
                results = []
                for company, filename in COMPANY_FILES.items():
                    success = process_company(conn, log_file, company, filename)
                    results.append(success)
                    log_step("-" * 50, log_file)  # Séparateur
                
                conn.commit()
                
                # Rapport final
                success_count = sum(results)
                total = len(COMPANY_FILES)
                if success_count == total:
                    log_step(f"✅ SUCCÈS COMPLET: {success_count}/{total} tables chargées", log_file)
                else:
                    log_step(f"⚠️ TERMINÉ AVEC AVERTISSEMENT: {success_count}/{total} tables chargées", log_file)
                
                return success_count == total

        except Exception as e:
            log_step(f"❌ ERREUR CRITIQUE: {str(e)}", log_file)
            raise

if __name__ == '__main__':
    if main():
        print("\nOpération terminée avec succès")
        exit(0)
    else:
        print("\nOpération terminée avec des erreurs")
        exit(1)