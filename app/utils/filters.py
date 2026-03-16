import streamlit as st
import pandas as pd


def init_filters(df: pd.DataFrame):
    """Initialise session-state keys so get_filtered_df() never crashes."""
    if "filter_countries" not in st.session_state:
        st.session_state["filter_countries"] = []
    if "filter_categories" not in st.session_state:
        st.session_state["filter_categories"] = []
    if "filter_contract_type" not in st.session_state:
        st.session_state["filter_contract_type"] = []
    if "filter_contract_time" not in st.session_state:
        st.session_state["filter_contract_time"] = []
    if "filter_salary_min" not in st.session_state:
        st.session_state["filter_salary_min"] = 0
    if "filter_salary_max" not in st.session_state:
        st.session_state["filter_salary_max"] = 300_000
    if "filter_text" not in st.session_state:
        st.session_state["filter_text"] = ""


def sidebar_filters(df: pd.DataFrame):
    """Render sidebar filter widgets and update session state."""
    with st.sidebar:
        st.header("Filters")

        # ── Country ──────────────────────────────────────────────────────────
        if "pais" in df.columns:
            countries = sorted(df["pais"].dropna().unique().tolist())
            st.session_state["filter_countries"] = st.multiselect(
                "Country",
                options=countries,
                default=st.session_state.get("filter_countries", []),
                key="ms_countries",
            )

        # ── Sector ───────────────────────────────────────────────────────────
        if "categoria_tag" in df.columns:
            cats = sorted([
                c for c in df["categoria_tag"].dropna().unique().tolist()
                if c not in ("unknown", "other-general-jobs")
            ])
            st.session_state["filter_categories"] = st.multiselect(
                "Sector",
                options=cats,
                default=st.session_state.get("filter_categories", []),
                key="ms_categories",
            )

        # ── Contract type ─────────────────────────────────────────────────────
        if "contract_type" in df.columns:
            ctypes = sorted(df["contract_type"].dropna().unique().tolist())
            st.session_state["filter_contract_type"] = st.multiselect(
                "Contract type",
                options=ctypes,
                default=st.session_state.get("filter_contract_type", []),
                key="ms_ctype",
            )

        # ── Contract time ─────────────────────────────────────────────────────
        if "contract_time" in df.columns:
            ctimes = sorted(df["contract_time"].dropna().unique().tolist())
            st.session_state["filter_contract_time"] = st.multiselect(
                "Contract time",
                options=ctimes,
                default=st.session_state.get("filter_contract_time", []),
                key="ms_ctime",
            )

        # ── Salary range ──────────────────────────────────────────────────────
        salary_mid = (
            pd.to_numeric(df.get("salary_min"), errors="coerce") +
            pd.to_numeric(df.get("salary_max"), errors="coerce")
        ) / 2
        sal_min = int(salary_mid.min(skipna=True) or 0)
        sal_max = int(salary_mid.max(skipna=True) or 300_000)

        sel = st.slider(
            "Annual salary range (€)",
            min_value=sal_min,
            max_value=sal_max,
            value=(
                max(st.session_state.get("filter_salary_min", sal_min), sal_min),
                min(st.session_state.get("filter_salary_max", sal_max), sal_max),
            ),
            step=1_000,
            key="sl_salary",
        )
        st.session_state["filter_salary_min"] = sel[0]
        st.session_state["filter_salary_max"] = sel[1]

        # ── Text search ────────────────────────────────────────────────────────
        st.session_state["filter_text"] = st.text_input(
            "Search title / company",
            value=st.session_state.get("filter_text", ""),
            key="txt_search",
        )


def get_filtered_df(df: pd.DataFrame) -> pd.DataFrame:
    """Apply session-state filters and return the filtered DataFrame."""
    f = df.copy()

    # Salary midpoint
    f["salary_mid"] = (
        pd.to_numeric(f.get("salary_min"), errors="coerce") +
        pd.to_numeric(f.get("salary_max"), errors="coerce")
    ) / 2

    # Country
    sel_countries = st.session_state.get("filter_countries", [])
    if sel_countries and "pais" in f.columns:
        f = f[f["pais"].isin(sel_countries)]

    # Sector
    sel_cats = st.session_state.get("filter_categories", [])
    if sel_cats and "categoria_tag" in f.columns:
        f = f[f["categoria_tag"].isin(sel_cats)]

    # Contract type
    sel_ctype = st.session_state.get("filter_contract_type", [])
    if sel_ctype and "contract_type" in f.columns:
        f = f[f["contract_type"].isin(sel_ctype)]

    # Contract time
    sel_ctime = st.session_state.get("filter_contract_time", [])
    if sel_ctime and "contract_time" in f.columns:
        f = f[f["contract_time"].isin(sel_ctime)]

    # Salary
    sal_min = st.session_state.get("filter_salary_min", 0)
    sal_max = st.session_state.get("filter_salary_max", 300_000)
    sal_mask = f["salary_mid"].isna() | f["salary_mid"].between(sal_min, sal_max)
    f = f[sal_mask]

    # Text search
    text_q = st.session_state.get("filter_text", "").strip().lower()
    if text_q:
        title_match   = f.get("title",   pd.Series([""] * len(f))).fillna("").str.lower().str.contains(text_q, na=False)
        company_match = f.get("company", pd.Series([""] * len(f))).fillna("").str.lower().str.contains(text_q, na=False)
        f = f[title_match | company_match]

    return f.reset_index(drop=True)
