import os
import sys
import time
import json
import logging
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Chargement des variables d'environnement
env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path=env_path)

BASE_DIR = os.getenv("BASE_DIR")
LOG_DIR = os.getenv("LOG_DIR")
TRUSTPILOT_DATA_DIR = os.path.join(BASE_DIR, "data", "trustpilot")

# Configuration du logging
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = os.path.join(LOG_DIR, "scraping_trustpilot.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Fonction principale
def scrap_trustpilot(societe_domaine):
    societe = societe_domaine.split(".")[0].lower()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    societe_dir = os.path.join(TRUSTPILOT_DATA_DIR, societe)
    os.makedirs(societe_dir, exist_ok=True)

    derniere_page_path = os.path.join(societe_dir, "derniere_page.txt")
    history_path = os.path.join(societe_dir, "history.txt")

    # Détection de la page de démarrage
    start_page = 1
    if os.path.exists(derniere_page_path):
        with open(derniere_page_path, "r") as f:
            try:
                start_page = int(f.read().strip()) + 1
            except:
                pass

    logging.info(f"Lancement scraping : société = {societe} | start_page = {start_page}")

    avis_list = []
    nb_pages = 0

    for page in range(start_page, start_page + 10):  # Limité à 10 pages pour test
        url = f"https://fr.trustpilot.com/review/{societe_domaine}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        avis_elements = soup.find_all("section", {"data-qa": "review"})

        if not avis_elements:
            break  # Fin des pages

        avis_page = []
        for avis in avis_elements:
            titre = avis.find("h2")
            texte = avis.find("p")
            note = avis.find("div", class_="star-rating_starRating__4rrcf").get("class", [])
            date = avis.find("time").get("datetime") if avis.find("time") else ""

            avis_page.append({
                "titre": titre.text.strip() if titre else "",
                "commentaire": texte.text.strip() if texte else "",
                "note": len(note) - 2,  # Hack simple pour étoile
                "date": date
            })

        avis_list.extend(avis_page)
        nb_pages += 1

        logging.info(f"Page {page} | URL: {url} | Avis : {len(avis_page)}")
        time.sleep(1)

    # Aucun avis
    if not avis_list:
        logging.warning("Aucun avis trouvé. Fin du script.")
        return

    # Sauvegarde
    scrap_dirname = f"scrap_{societe}_{now}"
    scrap_dir = os.path.join(societe_dir, scrap_dirname)
    os.makedirs(scrap_dir, exist_ok=True)

    # CSV
    csv_path = os.path.join(scrap_dir, f"{societe}_commentaires_{now}.csv")
    pd.DataFrame(avis_list).to_csv(csv_path, index=False)

    # JSON
    json_path = os.path.join(scrap_dir, f"{societe}_commentaires_{now}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(avis_list, f, ensure_ascii=False, indent=2)

    # Excel
    xlsx_path = os.path.join(scrap_dir, f"{societe}_commentaires_{now}.xlsx")
    pd.DataFrame(avis_list).to_excel(xlsx_path, index=False)

    # Informations générales
    txt_path = os.path.join(scrap_dir, f"{societe}_informations_generales_{now}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Société : {societe_domaine}\n")
        f.write(f"Nombre total d'avis : {len(avis_list)}\n")
        f.write(f"Nombre de pages scrapées : {nb_pages}\n")
        f.write(f"Heure : {datetime.now()}\n")

    # Mise à jour du fichier derniere_page.txt
    with open(derniere_page_path, "w") as f:
        f.write(str(start_page + nb_pages - 1))

    # Ajout au fichier history.txt
    with open(history_path, "a") as f:
        f.write(f"{now} | {scrap_dirname} | {len(avis_list)} avis\n")

    # Affichage utilisateur
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Données sauvegardées dans : {scrap_dir}")
    print("\nArborescence du répertoire :")
    print(f"├── derniere_page.txt")
    print(f"├── history.txt")
    print(f"└── {scrap_dirname}")
    for f in os.listdir(scrap_dir):
        print(f"    ├── {f}")

    logging.info(f"Données sauvegardées dans : {scrap_dir}")


# Lancement
if __name__ == "__main__":
    try:
        societe_domaine = input("Entrez le nom du domaine/société (ex. 'tesla.com') : ").strip()
        scrap_trustpilot(societe_domaine)
    except KeyboardInterrupt:
        print("\nInterruption utilisateur.")
