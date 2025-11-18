import requests
import mwparserfromhell
import re
import json
import os
import time
from urllib.parse import unquote
from dotenv import load_dotenv

# ===============================================================
# Chargement des variables d'environnement
# ===============================================================

load_dotenv()

BASE_DIR = os.getenv("BASE_DIR")
if not BASE_DIR:
    raise EnvironmentError("La variable BASE_DIR n'est pas définie dans le fichier .env")

# Dossier wikipedia
WIKI_DATA_DIR = os.path.join(BASE_DIR, "data", "wikipedia")
os.makedirs(WIKI_DATA_DIR, exist_ok=True)

# Mapping des entreprises → ID fichiers
SOCIETE_IDS = {
    "Chronopost": "1",
    "Vinted": "2",
    "Temu (marché)": "3",
    "Tesla (automobile)": "4"
}

# User-Agent obligatoire (Wikipédia refuse les requêtes sinon)
HEADERS = {
    "User-Agent": "Didier-CDE-Project/1.0 (contact: ditxx@gmail.com)"
}

# ===============================================================
# Nettoyage des textes Wikipédia
# ===============================================================

def clean_wikitext(text):
    text = str(text)
    text = re.sub(r"\[\[(?:[^|\]]+\|)?([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\{\{(?:[^|}]+|)*\|([^}]+)\}\}", r"\1", text)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()

# ===============================================================
# Fonction de requête Wikipédia avec retry + User-Agent
# ===============================================================

def safe_get_json(url, params, retries=3, delay=2):
    for i in range(retries):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=10)

            if response.status_code == 403:
                print("🚫 Accès refusé (403) — Vérifiez le User-Agent.")
                return None

            if response.status_code != 200:
                print(f"⚠️ HTTP {response.status_code}, tentative {i+1}/{retries}")
                time.sleep(delay)
                continue

            return response.json()

        except Exception as e:
            print(f"⚠️ Erreur réseau ({e}), tentative {i+1}/{retries}")
            time.sleep(delay)

    return None

# ===============================================================
# Scraping de l'infobox Wikipédia
# ===============================================================

def get_infobox(page_title):
    print(f"\n🔍 Traitement Wikipédia : {page_title}")

    params = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "revisions|pageprops",
        "rvprop": "content",
        "rvslots": "main",
    }

    data = safe_get_json("https://fr.wikipedia.org/w/api.php", params)

    if not data:
        return {"error": f"Impossible de récupérer {page_title}", "id_societe": SOCIETE_IDS.get(page_title, "")}

    page = next(iter(data["query"]["pages"].values()))

    if "missing" in page:
        return {"error": f"Page '{page_title}' non trouvée", "id_societe": SOCIETE_IDS.get(page_title, "")}

    try:
        wikitext = page["revisions"][0]["slots"]["main"]["*"]
    except Exception:
        return {"error": "Pas de contenu disponible", "id_societe": SOCIETE_IDS.get(page_title, "")}

    parsed = mwparserfromhell.parse(wikitext)

    infobox = {"id_societe": SOCIETE_IDS.get(page_title, "")}

    # Extraction de l'infobox
    for template in parsed.filter_templates():
        if "Infobox" in template.name:
            for param in template.params:
                key = clean_wikitext(param.name)
                value = clean_wikitext(param.value)
                infobox[key] = value
            break

    # Ajout du logo
    if "logo" in infobox:
        infobox["logo_url"] = get_image_url(infobox["logo"])

    return infobox

# ===============================================================
# Récupération URL du logo
# ===============================================================

def get_image_url(filename):
    filename = unquote(filename.split("|")[0].strip())

    params = {
        "action": "query",
        "format": "json",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
    }

    data = safe_get_json("https://fr.wikipedia.org/w/api.php", params)

    if not data:
        return ""

    page = next(iter(data["query"]["pages"].values()))
    return page.get("imageinfo", [{}])[0].get("url", "")

# ===============================================================
# TRAITEMENT DE TOUTES LES ENTREPRISES
# ===============================================================

entreprises = list(SOCIETE_IDS.keys())
results = {}

for entreprise in entreprises:

    data = get_infobox(entreprise)
    results[entreprise] = data

    filename = os.path.join(WIKI_DATA_DIR, f"{SOCIETE_IDS[entreprise]}_infobox.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"📁 Export : {filename}")

# Export global
global_file = os.path.join(WIKI_DATA_DIR, "entreprises_infobox.json")
with open(global_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("\n✅ Export global terminé :", global_file)