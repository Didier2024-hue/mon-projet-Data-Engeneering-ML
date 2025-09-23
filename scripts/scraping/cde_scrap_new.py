import os
import re
import time
import json
import logging
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv
from dateutil import parser

def resolve_env_vars(value, env_dict):
    if not value:
        return value
    pattern = re.compile(r"\$\{([^}]+)\}")
    matches = pattern.findall(value)
    for var in matches:
        if var in env_dict:
            value = value.replace(f"${{{var}}}", env_dict[var])
    return value

load_dotenv()
env_vars = dict(os.environ)

base_dir = env_vars.get("BASE_DIR", os.path.dirname(os.path.abspath(__file__)))
base_dir = resolve_env_vars(base_dir, env_vars)

data_raw_trustpilot = resolve_env_vars(env_vars.get("DATA_RAW_TRUSTPILOT"), env_vars)
if not data_raw_trustpilot:
    data_raw_trustpilot = os.path.join(base_dir, "data", "trustpilot")

log_dir = resolve_env_vars(env_vars.get("LOG_DIR"), env_vars)
if not log_dir:
    log_dir = os.path.join(base_dir, "log")

os.makedirs(data_raw_trustpilot, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"scraping_trustpilot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler()]
)

class TrustpilotScraper:
    def __init__(self, domain, max_pages=30):
        self.original_domain = domain.lower().strip()
        self.domain = re.sub(r"\.[a-z]{2,}$", "", self.original_domain)
        self.domain_dir = os.path.join(data_raw_trustpilot, self.domain)
        os.makedirs(self.domain_dir, exist_ok=True)
        self.max_pages = max_pages
        self.ua = UserAgent()
        self.session = self._init_session()
        self.last_page_path = os.path.join(self.domain_dir, "derniere_page.txt")
        self.info_data = None
        self.last_successful_page = 0

    def _init_session(self):
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=1, status_forcelist=[500,502,503,504])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('https://', adapter)
        return session

    def _headers(self):
        return {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.google.com/"
        }

    def _load_last_page(self):
        if os.path.exists(self.last_page_path):
            try:
                page = int(open(self.last_page_path, "r", encoding="utf-8").read().strip())
                logging.info(f"Reprise à partir de la page {page + 1}")
                return page + 1
            except Exception as e:
                logging.warning(f"Erreur lecture {self.last_page_path} : {e}")
        return 1

    def _save_last_page(self, page):
        try:
            with open(self.last_page_path, "w", encoding="utf-8") as f:
                f.write(str(page))
            self.last_successful_page = page
        except Exception as e:
            logging.error(f"Erreur sauvegarde {self.last_page_path} : {e}")

    def _extract_json_ld(self, soup):
        """
        Extraction robuste des informations générales :
        - secteur (name)
        - repartition des avis (csvw:columns)
        - nombre total d'avis (total dans la répartition ou somme)
        """
        try:
            script_ld = soup.find("script", type="application/ld+json", attrs={"data-business-unit-json-ld-dataset": "true"})
            if not script_ld:
                logging.warning("Aucun script ld+json trouvé.")
                return None
            data_ld = json.loads(script_ld.string)

            secteur = data_ld.get("@graph", {}).get("name", "Non renseigné")
            repartition = {}
            nombre_avis = "N/A"

            graph = data_ld.get("@graph")
            if graph:
                # Ici selon ta structure c'est un dict (pas liste) dans @graph, donc on adapte
                # Dans l'exemple que tu as donné, @graph est un dict avec mainEntity
                main_entity = graph.get("mainEntity")
                if main_entity:
                    table_schema = main_entity.get("csvw:tableSchema", {})
                    columns = table_schema.get("csvw:columns", [])
                    for col in columns:
                        nom_col = col.get("csvw:name", "")
                        cellules = col.get("csvw:cells", [])
                        if not cellules:
                            continue
                        try:
                            valeur = int(cellules[0].get("csvw:value", 0))
                        except Exception:
                            valeur = 0
                        repartition[nom_col] = valeur

                    if "Total" in repartition:
                        nombre_avis = repartition["Total"]
                    else:
                        nombre_avis = sum(v for k,v in repartition.items() if isinstance(v, int))

            else:
                logging.warning("Structure @graph manquante ou inattendue dans JSON-LD")

            # secteur dans name sous @graph ou dans racine ?
            # Tu avais dans ton exemple : "name": "Chronopost"
            secteur = data_ld.get("@graph", {}).get("name") or data_ld.get("name", "Non renseigné")

            return {
                "secteur": secteur,
                "repartition_avis": repartition,
                "nombre_avis": nombre_avis
            }
        except Exception as e:
            logging.error(f"Erreur extraction JSON-LD: {e}")
            return None

    def _extract_note_globale(self, soup):
        """
        Extraction note globale depuis meta property="og:title"
        """
        try:
            meta_og = soup.find("meta", property="og:title")
            if meta_og and meta_og.has_attr("content"):
                content = meta_og["content"]
                match = re.search(r"avec\s+([\d,\.]+)\s*/\s*5", content)
                if match:
                    note = match.group(1).replace(",", ".")
                    return note
            return "N/A"
        except Exception as e:
            logging.error(f"Erreur extraction note globale: {e}")
            return "N/A"

    def scrape(self):
        start_page = self._load_last_page()
        current_page = start_page
        all_reviews = []
        first_page_scraped = None
        consecutive_errors = 0

        while current_page < start_page + self.max_pages:
            url = f"https://fr.trustpilot.com/review/{self.original_domain}?page={current_page}"
            logging.info(f"Scraping page {current_page}: {url}")

            try:
                resp = self.session.get(url, headers=self._headers(), timeout=30)
                resp.raise_for_status()
                consecutive_errors = 0
            except requests.RequestException as e:
                logging.error(f"Erreur requête page {current_page} : {e}")
                consecutive_errors += 1
                if consecutive_errors > 3:
                    logging.error("Trop d'erreurs consécutives, arrêt du scraping")
                    break
                current_page += 1
                continue

            soup = BeautifulSoup(resp.text, "html.parser")

            if first_page_scraped is None:
                ld_data = self._extract_json_ld(soup)
                note_globale = self._extract_note_globale(soup)
                if not ld_data:
                    logging.warning("Impossible d'extraire JSON-LD, données générales incomplètes.")
                    ld_data = {"secteur": "Non renseigné", "repartition_avis": {}, "nombre_avis": "N/A"}
                self.info_data = {
                    "societe": self.original_domain,
                    "url": url,
                    "secteur": ld_data["secteur"],
                    "note_globale": note_globale,
                    "nombre_avis": ld_data["nombre_avis"],
                    "repartition_avis": ld_data["repartition_avis"],
                    "date_extraction": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nombre_commentaires": 0,
                    "pages_scrapees": ""
                }

            script_tag = soup.find("script", id="__NEXT_DATA__", type="application/json")
            if not script_tag:
                logging.error(f"Script __NEXT_DATA__ non trouvé page {current_page}, arrêt")
                break

            try:
                data = json.loads(script_tag.string)
                reviews = data["props"]["pageProps"].get("reviews", [])
                if first_page_scraped is None:
                    first_page_scraped = current_page
                if not reviews:
                    logging.info(f"Aucun avis trouvé page {current_page} -> fin scraping")
                    break
            except Exception as e:
                logging.error(f"Erreur parsing JSON page {current_page}: {e}")
                break

            page_reviews = []
            for rev in reviews:
                date_raw = rev.get("dates", {}).get("publishedDate")
                if date_raw:
                    try:
                        date_parsed = parser.isoparse(date_raw)
                        date_formatted = date_parsed.strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        date_formatted = date_raw
                else:
                    date_formatted = None

                r = {
                    "page": current_page,
                    "url_page": url,
                    "auteur": rev.get("consumer", {}).get("displayName"),
                    "date": date_formatted,
                    "commentaire": rev.get("text"),
                    "note_commentaire": str(rev.get("rating", ""))
                }
                page_reviews.append(r)

            all_reviews.extend(page_reviews)
            self._save_last_page(current_page)
            logging.info(f"Page {current_page} traitée, {len(page_reviews)} avis récupérés")

            sleep_time = 5 + (current_page % 6)
            logging.info(f"Pause {sleep_time} secondes avant page suivante...")
            time.sleep(sleep_time)

            current_page += 1

        if all_reviews:
            self._save_results(all_reviews, first_page_scraped if first_page_scraped else start_page)
            pages_range = f"-{first_page_scraped if first_page_scraped else start_page} à {self.last_successful_page}"
            self.info_data["pages_scrapees"] = pages_range
            self.info_data["nombre_commentaires"] = len(all_reviews)
        else:
            logging.warning("Aucun avis récupéré durant ce scraping.")

    def _save_results(self, reviews, first_page_scraped):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scrap_dir = os.path.join(self.domain_dir, f"scrap_{self.domain}_{timestamp}")
        os.makedirs(scrap_dir, exist_ok=True)

        try:
            path_info = os.path.join(scrap_dir, f"{self.domain}_informations_generales_{timestamp}.txt")
            with open(path_info, "w", encoding="utf-8") as f:
                json.dump(self.info_data, f, ensure_ascii=False, indent=4)
            logging.info(f"Informations générales sauvegardées dans {path_info}.")
        except Exception as e:
            logging.error(f"Erreur sauvegarde informations générales : {e}")

        df = pd.DataFrame(reviews)
        csv_path = os.path.join(scrap_dir, f"{self.domain}_commentaires_{timestamp}.csv")
        json_path = os.path.join(scrap_dir, f"{self.domain}_commentaires_{timestamp}.json")
        excel_path = os.path.join(scrap_dir, f"{self.domain}_commentaires_{timestamp}.xlsx")

        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)
        df.to_excel(excel_path, index=False)

        logging.info(f"Données sauvegardées dans {scrap_dir}")

def main():
    domain = input("Entrez le nom de domaine (ex: chronopost.fr) : ").strip()
    if not domain:
        logging.error("Le domaine ne peut pas être vide.")
        return
    max_pages_input = input("Nombre max de pages à scraper (défaut 30) : ").strip()
    max_pages = int(max_pages_input) if max_pages_input.isdigit() else 30

    scraper = TrustpilotScraper(domain, max_pages)
    scraper.scrape()

if __name__ == "__main__":
    main()
