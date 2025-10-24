# Exemple minimal pour récupérer le JSON
import requests
from fake_useragent import UserAgent

url = "https://fr.trustpilot.com/review/chronopost.fr?page=1"
headers = {'User-Agent': UserAgent().random}
resp = requests.get(url, headers=headers)
start = resp.text.find('<script id="__NEXT_DATA__" type="application/json">')
start += len('<script id="__NEXT_DATA__" type="application/json">')
end = resp.text.find('</script>', start)
json_str = resp.text[start:end]

with open("next_data.json", "w", encoding="utf-8") as f:
    f.write(json_str)
print("JSON sauvegardé dans next_data.json")

