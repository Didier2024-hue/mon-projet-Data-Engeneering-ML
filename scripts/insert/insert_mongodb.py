import os
import json
import re
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError

# Chargement du .env avec fallback silencieux
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = os.getenv("BASE_DIR", "/home/datascientest/cde")
SOCIETES_A_TRAITER = ['temu', 'tesla', 'chronopost', 'vinted']
LOG_DIR = os.path.join(BASE_DIR, "log")

def ensure_log_dir():
    """Crée le répertoire de logs si inexistant"""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def get_log_file():
    """Génère un nom de fichier de log avec timestamp"""
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(LOG_DIR, f"import_mongodb_{now}.log")

class Logger:
    """Logger personnalisé avec écriture console + fichier"""
    def __init__(self, filepath):
        self.filepath = filepath
        self.log_lines = []

    def log(self, msg, level="INFO"):
        """Ajoute un message de log avec timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_msg = f"[{timestamp}] {level} - {msg}"
        print(full_msg)
        self.log_lines.append(full_msg)

    def save(self):
        """Sauvegarde les logs dans le fichier"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(self.log_lines))

def trouver_fichier_info_generale(societe_path, societe_nom):
    """Trouve le fichier d'informations générales le plus récent"""
    pattern_dir = re.compile(rf"scrap_{societe_nom}_\d{{8}}(_\d+)?")
    pattern_file = re.compile(rf"{societe_nom}_informations_generales_\d{{8}}_\d{{6}}\.txt")

    candidats = []
    for entry in os.listdir(societe_path):
        full_path = os.path.join(societe_path, entry)
        if os.path.isdir(full_path) and pattern_dir.fullmatch(entry):
            for f in os.listdir(full_path):
                if pattern_file.fullmatch(f):
                    candidats.append(os.path.join(full_path, f))
    
    return max(candidats) if candidats else None

def convertir_repartition(repartition):
    """Convertit les clés de répartition en format standard"""
    return {
        "1": repartition.get("1 étoile"),
        "2": repartition.get("2 étoiles"),
        "3": repartition.get("3 étoiles"),
        "4": repartition.get("4 étoiles"),
        "5": repartition.get("5 étoiles"),
        "total": repartition.get("Total")
    }

def main():
    ensure_log_dir()
    log = Logger(get_log_file())

    mongo_uri = os.getenv("MONGO_URI")
    mongo_db = os.getenv("MONGO_DB")

    if not mongo_uri or not mongo_db:
        log.log("Configuration MongoDB manquante dans .env", "ERROR")
        log.log("Assurez-vous d'avoir MONGO_URI et MONGO_DB définis", "ERROR")
        log.save()
        return

    try:
        # Connexion à MongoDB avec vérification
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.server_info()  # Teste la connexion
        db = client[mongo_db]
        log.log(f"Connecté à MongoDB | Base: {mongo_db}", "SUCCESS")

        # Vidage des collections avant import (une seule fois au début)
        try:
            db.societe.delete_many({})
            db.avis_trustpilot.delete_many({})
            log.log("Collections vidées avec succès avant import", "INFO")
        except PyMongoError as e:
            log.log(f"Erreur lors du vidage des collections: {str(e)}", "ERROR")
            raise

        for soc in SOCIETES_A_TRAITER:
            societe_path = os.path.join(BASE_DIR, "data", "trustpilot", soc)
            if not os.path.isdir(societe_path):
                log.log(f"Dossier {societe_path} non trouvé, skip.", "WARNING")
                continue

            fichier_info = trouver_fichier_info_generale(societe_path, soc)
            if not fichier_info:
                log.log(f"Fichier infos générales introuvable pour '{soc}', skip.", "WARNING")
                continue

            log.log(f"Traitement de {fichier_info}", "INFO")
            
            try:
                with open(fichier_info, encoding='utf-8') as f:
                    societe_data = json.load(f)
            except json.JSONDecodeError as e:
                log.log(f"Erreur de lecture JSON pour {fichier_info}: {str(e)}", "ERROR")
                continue

            repartition = convertir_repartition(societe_data.get("repartition_avis", {}))

            # Insertion des données société
            try:
                db.societe.update_one(
                    {"nom": soc},
                    {"$set": {
                        "nom": societe_data.get("societe", soc),
                        "url": societe_data.get("url"),
                        "secteur": societe_data.get("secteur"),
                        "note_globale": float(societe_data.get("note_globale")) if societe_data.get("note_globale") else None,
                        "nombre_avis": int(societe_data.get("nombre_avis", 0)),
                        "note_1": repartition.get("1"),
                        "note_2": repartition.get("2"),
                        "note_3": repartition.get("3"),
                        "note_4": repartition.get("4"),
                        "note_5": repartition.get("5"),
                        "total_avis": repartition.get("total"),
                        "date_extraction": datetime.strptime(societe_data["date_extraction"], "%Y-%m-%d %H:%M:%S") if societe_data.get("date_extraction") else None,
                        "nombre_commentaires": int(societe_data.get("nombre_commentaires", 0)),
                        "pages_scrapees": societe_data.get("pages_scrapees", "")
                    }},
                    upsert=True
                )
            except PyMongoError as e:
                log.log(f"Erreur MongoDB lors de l'insertion pour {soc}: {str(e)}", "ERROR")
                continue
            except ValueError as e:
                log.log(f"Erreur de conversion de données pour {soc}: {str(e)}", "ERROR")
                continue

            # Traitement des avis
            pattern_dir = re.compile(rf"scrap_{soc}_\d{{8}}(_\d+)?")
            total_avis = 0
            repertoires_traite = set()

            for entry in sorted(os.listdir(societe_path)):
                full_path = os.path.join(societe_path, entry)
                if os.path.isdir(full_path) and pattern_dir.fullmatch(entry):
                    if entry in repertoires_traite:
                        log.log(f"Dossier déjà traité dans cette session: {entry}", "WARNING")
                        continue
                    repertoires_traite.add(entry)

                    log.log(f"Lecture dossier: {entry}", "INFO")

                    for file in os.listdir(full_path):
                        if file.endswith(".json") and not file.startswith(f"{soc}_informations_generales"):
                            file_path = os.path.join(full_path, file)
                            try:
                                with open(file_path, encoding='utf-8') as f:
                                    avis_list = json.load(f)
                                
                                # Ajout des métadonnées
                                for avis in avis_list:
                                    avis.update({
                                        "date_chargement": datetime.utcnow(),
                                        "id_societe": soc,
                                        "societe_nom": societe_data.get("societe", soc)
                                    })
                                
                                if avis_list:
                                    db.avis_trustpilot.insert_many(avis_list)
                                    total_avis += len(avis_list)
                            except json.JSONDecodeError as e:
                                log.log(f"Erreur JSON dans {file_path}: {str(e)}", "ERROR")
                            except PyMongoError as e:
                                log.log(f"Erreur MongoDB lors de l'insertion des avis {file_path}: {str(e)}", "ERROR")

            log.log(f"Société traitée: {soc} (Avis importés: {total_avis}, Répertoires traités: {len(repertoires_traite)})", "SUCCESS")

    except ConnectionFailure as e:
        log.log(f"Échec de connexion à MongoDB: {str(e)}", "ERROR")
    except PyMongoError as e:
        log.log(f"Erreur MongoDB: {str(e)}", "ERROR")
    except Exception as e:
        log.log(f"Erreur inattendue: {str(e)}", "ERROR")
    finally:
        if 'client' in locals():
            client.close()
            log.log("Connexion MongoDB fermée", "INFO")
        log.save()

if __name__ == "__main__":
    main()