# export_service.py
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

EXPORT_DIR = os.getenv("DATA_API", "/home/datascientest/cde/data/api")
os.makedirs(EXPORT_DIR, exist_ok=True)

def save_to_file(data: list, filename_base: str, formats: list = ["csv", "json", "xlsx"]):
    """
    Sauvegarde une liste de dicts dans CSV, JSON et/ou XLSX.
    Retourne les chemins complets des fichiers créés.
    """
    if not data:
        return {}

    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_paths = {}

    if "csv" in formats:
        path_csv = os.path.join(EXPORT_DIR, f"{filename_base}_{timestamp}.csv")
        df.to_csv(path_csv, index=False, encoding="utf-8")
        file_paths["csv"] = path_csv

    if "json" in formats:
        path_json = os.path.join(EXPORT_DIR, f"{filename_base}_{timestamp}.json")
        df.to_json(path_json, orient="records", force_ascii=False)
        file_paths["json"] = path_json

    if "xlsx" in formats:
        path_xlsx = os.path.join(EXPORT_DIR, f"{filename_base}_{timestamp}.xlsx")
        df.to_excel(path_xlsx, index=False)
        file_paths["xlsx"] = path_xlsx

    return file_paths
