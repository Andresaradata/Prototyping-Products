import os, json, requests
import pandas as pd
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

def get_count_for_category(country: str, category_tag: str):
    # Solo pedimos count; 1 resultado para minimizar carga
    url = f"{BASE}/jobs/{country}/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 1,
        "content-type": "application/json",
        "category": category_tag,
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json().get("count", 0)

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    rows = []
    for country in COUNTRIES:
        cats = get_categories(country)
        for c in cats:
            tag = c.get("tag")
            label = c.get("label")
            count = get_count_for_category(country, tag)
            rows.append({"pais": country, "categoria_tag": tag, "categoria_label": label, "count": count})
        print(f"OK {country}")

    df = pd.DataFrame(rows).sort_values(["pais", "count"], ascending=[True, False])
    df.to_csv("data/volumen_por_categoria.csv", index=False, encoding="utf-8")
    print("OK -> data/volumen_por_categoria.csv")