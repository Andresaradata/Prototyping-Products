import os
import time
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE = "https://api.adzuna.com/v1/api"

PAISES = ["es", "fr", "de", "nl", "gb", "ch"]

CATEGORIAS = [
    "it-jobs",
    "engineering-jobs",
    "accounting-finance-jobs",
    "logistics-warehouse-jobs",
    "manufacturing-jobs",
    "healthcare-nursing-jobs",
    "trade-construction-jobs",
    "sales-jobs",
    "teaching-jobs",
    "hospitality-catering-jobs",
]

RESULTS_PER_PAGE = 50
DIAS_ATRAS = 730  # 2 años
MAX_PAGINAS_POR_CATEGORIA = 400  # cinturón de seguridad

def parse_created(s: str) -> datetime:
    # ejemplo: 2026-02-22T18:08:56Z
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def adzuna_get(url: str, params: dict, max_retries: int = 6):
    for attempt in range(max_retries):
        r = requests.get(url, params=params, timeout=60)
        if r.status_code == 200:
            return r
        # Rate limit o error temporal
        if r.status_code in (429, 500, 502, 503, 504):
            sleep_s = min(2 ** attempt, 30)
            time.sleep(sleep_s)
            continue
        # Error no recuperable
        r.raise_for_status()
    r.raise_for_status()

def fetch_page(country: str, category_tag: str, page: int):
    url = f"{BASE}/jobs/{country}/search/{page}"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "content-type": "application/json",
        "results_per_page": RESULTS_PER_PAGE,
        "sort_by": "date",
        "category": category_tag,
    }
    r = adzuna_get(url, params=params)
    return r.json()

def flatten_job(country: str, job: dict) -> dict:
    cat = job.get("category") or {}
    comp = job.get("company") or {}
    loc = job.get("location") or {}

    return {
        "pais": country,
        "anuncio_id": str(job.get("id")),
        "created": job.get("created"),
        "title": job.get("title"),
        "description": job.get("description"),
        "categoria_tag": cat.get("tag"),
        "categoria_label": cat.get("label"),
        "company": comp.get("display_name"),
        "location_display": loc.get("display_name"),
        "location_area": "|".join(loc.get("area") or []),
        "latitude": job.get("latitude"),
        "longitude": job.get("longitude"),
        "contract_type": job.get("contract_type"),
        "contract_time": job.get("contract_time"),
        "salary_min": job.get("salary_min"),
        "salary_max": job.get("salary_max"),
        "salary_is_predicted": job.get("salary_is_predicted"),
        "redirect_url": job.get("redirect_url"),
        "adref": job.get("adref"),
    }

def quarter_from_created(created_iso: str) -> str:
    dt = parse_created(created_iso)
    q = (dt.month - 1) // 3 + 1
    return f"{dt.year}-Q{q}"

if __name__ == "__main__":
    if not APP_ID or not APP_KEY:
        raise SystemExit("Faltan ADZUNA_APP_ID / ADZUNA_APP_KEY en .env")

    cutoff = datetime.now(timezone.utc) - timedelta(days=DIAS_ATRAS)

    os.makedirs("data/raw", exist_ok=True)

    total_written = 0

    for country in PAISES:
        for cat in CATEGORIAS:
            out_path = f"data/raw/anuncios_{country}_{cat}.parquet"

            # Si ya existe, lo saltamos (para reanudar sin dolor)
            if os.path.exists(out_path):
                print("SKIP existe:", out_path)
                continue

            rows = []
            page = 1
            stop = False

            # barra de progreso por categoría
            pbar = tqdm(total=0, desc=f"{country}/{cat}", unit="anuncios")

            while not stop and page <= MAX_PAGINAS_POR_CATEGORIA:
                payload = fetch_page(country, cat, page)
                results = payload.get("results", [])

                if not results:
                    break

                for job in results:
                    created = parse_created(job.get("created"))
                    if created < cutoff:
                        stop = True
                        break
                    rows.append(flatten_job(country, job))

                pbar.total += len(results)
                pbar.update(len(results))

                page += 1
                time.sleep(0.25)  # suave con el servidor

            pbar.close()

            if rows:
                df = pd.DataFrame(rows).drop_duplicates(subset=["pais", "anuncio_id"])
                # Agregamos trimestre aquí mismo (útil para control)
                df["trimestre"] = df["created"].apply(quarter_from_created)

                df.to_parquet(out_path, index=False)
                total_written += len(df)
                print(f"OK -> {out_path} | filas: {len(df)}")
            else:
                # Guardamos vacío para no reintentar eternamente
                pd.DataFrame([]).to_parquet(out_path, index=False)
                print(f"OK -> {out_path} | filas: 0")

    print("FIN. Total filas (aprox):", total_written)