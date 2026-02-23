import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE = "https://api.adzuna.com/v1/api"

COUNTRIES = ["es", "fr", "de", "nl", "gb", "ch"]

# usamos 1 categoría común para la prueba; luego lo haremos por categoría
CATEGORY = "it-jobs"

def search_one(country: str):
    url = f"{BASE}/jobs/{country}/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 10,
        "content-type": "application/json",
        "category": CATEGORY,
        "sort_by": "date",
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    summary = {}
    for c in COUNTRIES:
        payload = search_one(c)
        results = payload.get("results", [])
        keys = sorted(set().union(*[set(x.keys()) for x in results])) if results else []
        summary[c] = {
            "count": payload.get("count"),
            "anuncios_en_pagina": len(results),
            "keys_anuncio": keys,
            "muestra": results[0] if results else None
        }
        print(c, "count=", payload.get("count"), "| keys=", len(keys))

    with open("data/probe_campos.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("OK -> data/probe_campos.json")