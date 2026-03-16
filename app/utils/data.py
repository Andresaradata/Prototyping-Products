from __future__ import annotations
import os
import glob
import pandas as pd
import streamlit as st

# ── Paths ─────────────────────────────────────────────────────────────────────
RAW_GLOB     = os.path.join("data", "raw", "anuncios_*.parquet")
ES_GLOB      = os.path.join("data", "raw", "anuncios_es_*.parquet")
MASTER_PATH  = os.path.join("data", "processed", "anuncios_master.parquet")

# ── Sector label map ──────────────────────────────────────────────────────────
SECTOR_LABELS = {
    "it-jobs":                   "IT & Technology",
    "engineering-jobs":          "Engineering",
    "accounting-finance-jobs":   "Accounting & Finance",
    "healthcare-nursing-jobs":   "Healthcare & Nursing",
    "hospitality-catering-jobs": "Hospitality & Catering",
    "logistics-warehouse-jobs":  "Logistics & Warehouse",
    "manufacturing-jobs":        "Manufacturing",
    "sales-jobs":                "Sales",
    "teaching-jobs":             "Teaching & Education",
    "trade-construction-jobs":   "Trade & Construction",
}


def _sector_from_path(path: str) -> str:
    """Extract sector slug from filename like 'anuncios_es_it-jobs.parquet'."""
    stem  = os.path.splitext(os.path.basename(path))[0]  # anuncios_es_it-jobs
    parts = stem.split("_", 2)                            # ['anuncios','es','it-jobs']
    return parts[2] if len(parts) == 3 else "unknown"


def _clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise types shared across all loaders."""
    df.columns = df.columns.str.strip().str.lower()

    for col in ("salary_min", "salary_max"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    for col in ("latitude", "longitude"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "created" in df.columns:
        df["created"] = pd.to_datetime(df["created"], errors="coerce", utc=True)

    return df


# ── Cached loaders ────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_spain_all() -> pd.DataFrame:
    """
    Load ALL anuncios_es_*.parquet files and merge them into one DataFrame.
    Adds a `sector_label` column so pages can filter/group by sector.
    This is the preferred loader — more data = better model.
    """
    files = sorted(glob.glob(ES_GLOB))
    if not files:
        return pd.DataFrame()

    frames = []
    for f in files:
        try:
            df = pd.read_parquet(f)
            df = _clean_df(df)
            slug  = _sector_from_path(f)
            df["sector_label"] = SECTOR_LABELS.get(slug, slug)
            frames.append(df)
        except Exception:
            continue

    if not frames:
        return pd.DataFrame()

    out = pd.concat(frames, ignore_index=True)

    # Deduplicate on anuncio_id if present
    if "anuncio_id" in out.columns:
        out = out.drop_duplicates(subset=["anuncio_id"])

    return out.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_raw_sample(limit_files: int = 6, limit_rows: int = 50_000) -> pd.DataFrame:
    """
    Fallback: load a sample of raw files when the Spain-specific ones aren't found.
    Same behaviour as before so nothing breaks.
    """
    files = sorted(glob.glob(RAW_GLOB))[:limit_files]
    if not files:
        return pd.DataFrame()

    frames = []
    for f in files:
        try:
            df = pd.read_parquet(f)
            df = _clean_df(df)
            slug = _sector_from_path(f)
            df["sector_label"] = SECTOR_LABELS.get(slug, slug)
            frames.append(df)
        except Exception:
            continue

    if not frames:
        return pd.DataFrame()

    out = pd.concat(frames, ignore_index=True)
    if len(out) > limit_rows:
        out = out.sample(limit_rows, random_state=42)

    return out.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_master() -> pd.DataFrame:
    """Load the consolidated master file if it exists."""
    if not os.path.exists(MASTER_PATH):
        return pd.DataFrame()
    df = pd.read_parquet(MASTER_PATH)
    return _clean_df(df)


def get_best_available_df() -> pd.DataFrame:
    """
    Priority order:
      1. Master file (if it exists)
      2. All Spain sector parquet files merged
      3. Any raw parquet files (sample fallback)
    """
    master = load_master()
    if not master.empty:
        return master

    spain = load_spain_all()
    if not spain.empty:
        return spain

    return load_raw_sample()
