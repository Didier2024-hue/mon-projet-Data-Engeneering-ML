import subprocess
import time

# 🔧 Paramètres à ajuster
total_pages = 177
pages_par_lancement = 30
delai_minutes = 3
nom_domaine = "temu.com"

page_courante = 1

while page_courante <= total_pages:
    print(f"=== Lancement du scraping : pages {page_courante} à {min(page_courante + pages_par_lancement - 1, total_pages)} ===")

    # Simuler les inputs du script interactif
    inputs = f"{nom_domaine}\n{pages_par_lancement}\n"

    try:
        subprocess.run(
            ["python3", "cde_scrap_new.py"], 
            input=inputs.encode(),
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du scraping : {e}")
        break

    page_courante += pages_par_lancement

    if page_courante <= total_pages:
        print(f"⏳ Attente de {delai_minutes} minutes avant prochain run...")
        time.sleep(delai_minutes * 60)

print("✅ Scraping terminé sur 1000 pages.")

