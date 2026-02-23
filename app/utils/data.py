from __future__ import annotations
import os
import glob
import pandas as pd
import streamlit as st

RAW_GLOB = os.path.join("data", "raw", "anuncios_*.parquet")
MASTER_PATH = os.path.join("data", "processed", "anuncios_master.parquet")

@st.cache_data(show_spinner=False)
def load_raw_sample(limit_files: int = 6, limit_rows: int = 50_000) -> pd.DataFrame:
    """Carga una muestra de archivos raw para que la app funcione aun sin master."""
    files = sorted(glob.glob(RAW_GLOB))[:limit_files]
    if not files:
        return pd.DataFrame()
    dfs = []
    for f in files:
        try:
            df = pd.read_parquet(f)
            dfs.append(df)
        except Exception:
            continue
    if not dfs:
        return pd.DataFrame()
    out = pd.concat(dfs, ignore_index=True)
    if len(out) > limit_rows:
        out = out.sample(limit_rows, random_state=42)
    return out

@st.cache_data(show_spinner=False)
def load_master() -> pd.DataFrame:
    """Carga el master consolidado si existe."""
    if not os.path.exists(MASTER_PATH):
        return pd.DataFrame()
    return pd.read_parquet(MASTER_PATH)

def get_best_available_df() -> pd.DataFrame:
    """Prioriza master; si no existe, usa muestra raw."""
    df = load_master()
    if not df.empty:
        return df
    return load_raw_sample()