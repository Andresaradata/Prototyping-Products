import os, json, requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE = "https://api.adzuna.com/v1/api"

COUNTRIES = ["es", "fr", "de", "nl", "gb", "ch"]

def get_categories(country: str):
    url = f"{BASE}/jobs/{country}/categories"
    params = {"app_id": APP_ID, "app_key": APP_KEY, "content-type": "application/json"}
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()["results"]

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    out = {}
    for c in COUNTRIES:
        cats = get_categories(c)
        out[c] = cats
        print(f"{c}: {len(cats)} categorias")

    with open("data/categorias_por_pais.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("OK -> data/categorias_por_pais.json")