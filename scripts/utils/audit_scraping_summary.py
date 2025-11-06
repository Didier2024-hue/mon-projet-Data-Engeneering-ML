import os
import json
from datetime import datetime

BASE_DIR = "/home/datascientest/cde/data/trustpilot"
OUTPUT_FILE = "/home/datascientest/cde/logs/audit_scraping_summary.json"

def is_json_file(filename):
    """Ne garde que les fichiers avec extension .json"""
    return filename.endswith(".json")

def audit_scraping_summary(base_dir):
    total_files = 0
    valid_files = 0
    invalid_files = 0
    invalid_list = []

    for root, _, files in os.walk(base_dir):
        for fname in files:
            if not is_json_file(fname):
                continue

            total_files += 1
            fpath = os.path.join(root, fname)

            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Vérifie format attendu (liste d’objets)
                if isinstance(data, list) and all(isinstance(x, dict) for x in data):
                    valid_files += 1
                else:
                    invalid_files += 1
                    invalid_list.append({"file": fpath, "reason": "structure non conforme"})
            except Exception as e:
                invalid_files += 1
                invalid_list.append({"file": fpath, "reason": str(e)})

    if total_files == 0:
        print("⚠️ Aucun fichier JSON trouvé.")
        return

    # Calcul du pourcentage exploitable
    valid_pct = round(valid_files / total_files * 100, 2)
    invalid_pct = 100 - valid_pct

    summary = {
        "audit_date": datetime.utcnow().isoformat(),
        "base_dir": base_dir,
        "total_files": total_files,
        "valid_files": valid_files,
        "invalid_files": invalid_files,
        "valid_pct": valid_pct,
        "invalid_pct": invalid_pct,
        "invalid_examples": invalid_list[:10],  # garder les 10 premiers fichiers invalides
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n📊 Résumé d’audit des fichiers Trustpilot")
    print("──────────────────────────────────────────────")
    print(f"📁 Dossier analysé     : {base_dir}")
    print(f"📦 Fichiers JSON       : {total_files}")
    print(f"✅ Fichiers valides    : {valid_files} ({valid_pct} %)")
    print(f"❌ Fichiers invalides  : {invalid_files} ({invalid_pct} %)")
    print(f"📝 Rapport détaillé    : {OUTPUT_FILE}")
    if invalid_files > 0:
        print("\n⚠️  Exemples de fichiers problématiques :")
        for entry in invalid_list[:5]:
            print(f"   - {entry['file']} ({entry['reason'][:60]}...)")

if __name__ == "__main__":
    audit_scraping_summary(BASE_DIR)

