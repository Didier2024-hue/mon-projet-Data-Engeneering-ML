import os
import json
import re
from datetime import datetime
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration
DATA_RAW_TRUSTPILOT = os.getenv("DATA_RAW_TRUSTPILOT")
LOG_DIR = os.getenv("LOG_DIR")
SOCIETES_A_TRAITER = ['temu', 'tesla', 'chronopost', 'vinted']

class Logger:
    def __init__(self, filepath):
        self.filepath = filepath
        self.log_lines = []
    
    def print(self, msg):
        print(msg)
        self.log_lines.append(msg)
    
    def save(self):
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(self.log_lines))
        except Exception as e:
            print(f"Erreur sauvegarde log : {e}")

def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def get_log_file():
    return os.path.join(LOG_DIR, f"import_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def connect_db():
    try:
        return psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT")
        )
    except OperationalError as e:
        raise RuntimeError(f"Erreur connexion PostgreSQL : {e}")

def truncate_tables(cur, logger):
    try:
        cur.execute("TRUNCATE TABLE avis_trustpilot, societe CASCADE;")
        logger.print("🗑️ Tables vidées (avis_trustpilot et societe)")
    except Exception as e:
        logger.print(f"Erreur TRUNCATE tables : {e}")
        raise

def safe_int(val):
    if val is None:
        return 0
    if isinstance(val, (int, float)):
        return int(val)
    try:
        cleaned = ''.join(c for c in str(val) if c.isdigit() or c in '.-')
        return int(float(cleaned.split()[0])) if cleaned.split() else 0
    except (ValueError, TypeError):
        return 0

def insert_societe(cur, societe_data, logger):
    repartition = societe_data.get("repartition_avis", {})
    
    notes = {
        '1': safe_int(repartition.get("1") or repartition.get("1 étoile") or repartition.get("1 star")),
        '2': safe_int(repartition.get("2") or repartition.get("2 étoiles") or repartition.get("2 stars")),
        '3': safe_int(repartition.get("3") or repartition.get("3 étoiles") or repartition.get("3 stars")),
        '4': safe_int(repartition.get("4") or repartition.get("4 étoiles") or repartition.get("4 stars")),
        '5': safe_int(repartition.get("5") or repartition.get("5 étoiles") or repartition.get("5 stars"))
    }

    date_extraction = None
    if societe_data.get("date_extraction"):
        try:
            date_extraction = datetime.strptime(societe_data["date_extraction"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            logger.print(f"⚠ Format date invalide : {societe_data.get('date_extraction')}")

    try:
        cur.execute("""
            INSERT INTO societe (
                nom, url, secteur, note_globale, nombre_avis,
                note_1, note_2, note_3, note_4, note_5,
                date_extraction, nombre_commentaires
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_societe;
        """, (
            societe_data["societe"],
            societe_data.get("url"),
            societe_data.get("secteur"),
            safe_int(societe_data.get("note_globale")),
            safe_int(societe_data.get("nombre_avis")),
            notes['1'], notes['2'], notes['3'], notes['4'], notes['5'],
            date_extraction,
            safe_int(societe_data.get("nombre_commentaires", 0))
        ))
        return cur.fetchone()[0]
    except Exception as e:
        logger.print(f"❌ Erreur insertion société {societe_data.get('societe')}: {e}")
        raise

def insert_avis(cur, id_societe, avis, logger):
    try:
        date_avis = datetime.strptime(avis["date"], "%Y-%m-%d %H:%M:%S") if avis.get("date") else None
    except ValueError:
        date_avis = None
        logger.print(f"⚠ Format date avis invalide : {avis.get('date')}")

    try:
        cur.execute("""
            INSERT INTO avis_trustpilot (
                id_societe, page, url_page, auteur, date_avis, 
                commentaire, note_commentaire, date_chargement
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            id_societe,
            avis.get("page"),
            avis.get("url_page"),
            avis.get("auteur"),
            date_avis,
            avis.get("commentaire"),
            safe_int(avis.get("note_commentaire")),
            datetime.utcnow()
        ))
    except Exception as e:
        logger.print(f"❌ Erreur insertion avis (ID société {id_societe}): {e}")
        raise

def trouver_fichier_info_generale(societe_path, societe_nom):
    pattern = re.compile(rf"{societe_nom}_informations_generales_\d{{8}}_\d{{6}}\.txt")
    candidats = [
        os.path.join(root, f)
        for root, _, files in os.walk(societe_path)
        for f in files if pattern.fullmatch(f)
    ]
    return max(candidats) if candidats else None

def compter_commentaires(societe_path, societe_nom, logger):
    total = 0
    pattern_dir = re.compile(rf"scrap_{societe_nom}_\d{{8}}(_\d+)?")
    
    for root, dirs, files in os.walk(societe_path):
        if pattern_dir.fullmatch(os.path.basename(root)):
            for file in files:
                if file.endswith('.json') and not file.startswith(f"{societe_nom}_informations_generales"):
                    try:
                        with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            total += len(data)
                    except Exception as e:
                        logger.print(f"⚠ Erreur lecture {file}: {e}")
    return total

def traiter_societe(soc, data_dir, logger, conn):
    societe_path = os.path.join(data_dir, soc)
    if not os.path.isdir(societe_path):
        logger.print(f"⚠ Dossier {soc} introuvable - skip")
        return 0

    fichier_info = trouver_fichier_info_generale(societe_path, soc)
    if not fichier_info:
        logger.print(f"⚠ Fichier info {soc} introuvable - skip")
        return 0

    try:
        with open(fichier_info, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data["societe"] = soc
    except Exception as e:
        logger.print(f"❌ Erreur lecture {fichier_info}: {e}")
        return 0

    try:
        with conn.cursor() as cur:
            total_commentaires = compter_commentaires(societe_path, soc, logger)
            data["nombre_commentaires"] = total_commentaires
            
            id_societe = insert_societe(cur, data, logger)
            logger.print(f"\n🔍 Traitement {soc} (ID: {id_societe})")
            logger.print(f"📊 Commentaires totaux: {total_commentaires}")

            total_avis = 0
            pattern_dir = re.compile(rf"scrap_{soc}_\d{{8}}(_\d+)?")

            # Liste des répertoires de scrap triés par date
            scrap_dirs = sorted([
                d for d in os.listdir(societe_path) 
                if os.path.isdir(os.path.join(societe_path, d)) and pattern_dir.fullmatch(d)
            ], key=lambda x: os.path.getmtime(os.path.join(societe_path, x)), reverse=True)

            for scrap_dir in scrap_dirs:
                scrap_path = os.path.join(societe_path, scrap_dir)
                avis_dir = 0
                
                # Compter les fichiers JSON dans ce répertoire
                json_files = [
                    f for f in os.listdir(scrap_path) 
                    if f.endswith('.json') and not f.startswith(f"{soc}_informations_generales")
                ]
                
                for file in json_files:
                    try:
                        with open(os.path.join(scrap_path, file), 'r', encoding='utf-8') as f:
                            avis_list = json.load(f)
                            for avis in avis_list:
                                insert_avis(cur, id_societe, avis, logger)
                                avis_dir += 1
                    except Exception as e:
                        logger.print(f"⚠ Erreur fichier {file}: {e}")
                        conn.rollback()  # Rollback seulement la transaction courante
                        continue  # Passe au fichier suivant
                
                total_avis += avis_dir
                logger.print(f"   📂 {scrap_dir}: {avis_dir} avis chargés")

            conn.commit()
            logger.print(f"✅ {soc}: {total_avis} avis importés au total\n")
            return total_avis

    except Exception as e:
        logger.print(f"❌ Erreur traitement {soc}: {e}")
        conn.rollback()
        return 0

def main():
    ensure_log_dir()
    logger = Logger(get_log_file())

    try:
        conn = connect_db()
        logger.print("⚡ Début importation données TrustPilot")

        # TRUNCATE une seule fois au début
        with conn.cursor() as cur:
            truncate_tables(cur, logger)
        conn.commit()

        total_avis = 0
        for societe in SOCIETES_A_TRAITER:
            total_avis += traiter_societe(societe, DATA_RAW_TRUSTPILOT, logger, conn)

        logger.print(f"🏁 Import terminé avec succès | Total avis: {total_avis}")
    except Exception as e:
        logger.print(f"💥 ERREUR GLOBALE: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()
        logger.save()

if __name__ == "__main__":
    main()