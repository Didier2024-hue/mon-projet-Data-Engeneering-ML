import requests
import mwparserfromhell
import re
import json
import os
from urllib.parse import unquote
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()

BASE_DIR = os.getenv("BASE_DIR")
if not BASE_DIR:
    raise EnvironmentError("La variable BASE_DIR n'est pas définie dans le fichier .env")

# Chemin du dossier wikipedia sous data/
WIKI_DATA_DIR = os.path.join(BASE_DIR, "data", "wikipedia")
os.makedirs(WIKI_DATA_DIR, exist_ok=True)

SOCIETE_IDS = {
    "Temu (marché)": "1",
    "Tesla (automobile)": "2",
    "Chronopost": "3",
    "Vinted": "4"
}

def clean_wikitext(text):
    text = str(text)
    text = re.sub(r"\[\[(?:[^|\]]+\|)?([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\{\{(?:[^|}]+|)*\|([^}]+)\}\}", r"\1", text)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\{\{formatnum:(\d+)\}\}", r"\1", text)
    text = re.sub(r"\{\{drapeau\|([^}]+)\}\}", r"\1", text)
    text = re.sub(r"\{\{lang\|[^|]+\|([^}]+)\}\}", r"\1", text)
    return text.strip()

def get_infobox(page_title):
    url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "revisions|pageprops",
        "rvprop": "content",
        "rvslots": "main",
    }
    response = requests.get(url, params=params)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    if "missing" in page:
        return {"error": f"Page '{page_title}' non trouvée"}
    wikitext = page["revisions"][0]["slots"]["main"]["*"]
    parsed = mwparserfromhell.parse(wikitext)
    infobox = {}
    infobox["id_societe"] = SOCIETE_IDS.get(page_title, "")
    for template in parsed.filter_templates():
        if "Infobox" in template.name:
            for param in template.params:
                key = clean_wikitext(param.name.strip())
                value = clean_wikitext(param.value.strip())
                infobox[key] = value
            break
    if "SIREN" not in infobox or not infobox.get("SIREN"):
        wikidata_id = page.get("pageprops", {}).get("wikibase_item")
        if wikidata_id:
            siren = get_siren_from_wikidata(wikidata_id)
            if siren:
                infobox["SIREN"] = siren
    if "logo" in infobox:
        infobox["logo_url"] = get_image_url(infobox["logo"])
    return infobox

def get_siren_from_wikidata(wikidata_id):
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={wikidata_id}&format=json&props=claims"
    response = requests.get(url)
    data = response.json()
    try:
        return data["entities"][wikidata_id]["claims"]["P1616"][0]["mainsnak"]["datavalue"]["value"]
    except (KeyError, IndexError):
        return None

def get_image_url(filename):
    filename = unquote(filename.split("|")[0].strip())
    url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": f"File:{filename}",
        "prop": "imageinfo",
        "iiprop": "url",
    }
    response = requests.get(url, params=params)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    return page.get("imageinfo", [{}])[0].get("url", "")

entreprises = [
    "Chronopost",
    "Vinted",
    "Temu (marché)",
    "Tesla (automobile)"
]

results = {}
for entreprise in entreprises:
    print(f"\n🔍 Traitement de : {entreprise}")
    data = get_infobox(entreprise)
    results[entreprise] = data

    filename = os.path.join(WIKI_DATA_DIR, f"{SOCIETE_IDS[entreprise]}_infobox.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)
    print(f"✅ Fichier créé : {filename}")

global_filename = os.path.join(WIKI_DATA_DIR, "entreprises_infobox.json")
with open(global_filename, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4, sort_keys=True)

print("\n✅ Export terminé :")
print(f"- Fichiers individuels : {WIKI_DATA_DIR}/1_infobox.json, 2_infobox.json, etc.")
print(f"- Fichier global : {WIKI_DATA_DIR}/entreprises_infobox.json")
