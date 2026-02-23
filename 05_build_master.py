import os
import glob
import pandas as pd

RAW_GLOB = os.path.join("data", "raw", "anuncios_*.parquet")
OUT_DIR = os.path.join("data", "processed")
OUT_PATH = os.path.join(OUT_DIR, "anuncios_master.parquet")

def quarter_from_created(created_series: pd.Series) -> pd.Series:
    dt = pd.to_datetime(created_series, errors="coerce", utc=True)
    q = ((dt.dt.month - 1) // 3 + 1).astype("Int64")
    return dt.dt.year.astype("Int64").astype(str) + "-Q" + q.astype(str)

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)

    files = sorted(glob.glob(RAW_GLOB))
    if not files:
        raise SystemExit("No raw files found in data/raw (anuncios_*.parquet).")

    dfs = []
    total_rows = 0

    for f in files:
        try:
            df = pd.read_parquet(f)
        except Exception as e:
            print("SKIP (read error):", f, "|", e)
            continue

        if df.empty:
            continue

        # Ensure required columns exist (safe defaults)
        if "pais" not in df.columns:
            df["pais"] = None
        if "categoria_tag" not in df.columns:
            df["categoria_tag"] = None
        if "created" not in df.columns:
            df["created"] = None
        if "anuncio_id" not in df.columns:
            # fallback if a different schema slipped in
            if "id" in df.columns:
                df["anuncio_id"] = df["id"].astype(str)
            else:
                df["anuncio_id"] = None

        # Add quarter if missing
        if "trimestre" not in df.columns:
            df["trimestre"] = quarter_from_created(df["created"])

        dfs.append(df)
        total_rows += len(df)

    if not dfs:
        raise SystemExit("No non-empty parquet files found to merge.")

    master = pd.concat(dfs, ignore_index=True)

    # Deduplicate by (pais, anuncio_id)
    master["anuncio_id"] = master["anuncio_id"].astype(str)
    master = master.drop_duplicates(subset=["pais", "anuncio_id"])

    # Basic cleanup: drop noisy categories if desired (optional)
    # master = master[~master["categoria_tag"].isin(["unknown", "other-general-jobs"])]

    master.to_parquet(OUT_PATH, index=False)
    print("OK ->", OUT_PATH)
    print("Rows:", len(master))
    print("Files merged:", len(files))