import streamlit as st
import pandas as pd

EXCLUDE_CATS = {"unknown", "other-general-jobs"}

def init_filters(df: pd.DataFrame):
    # Defaults (Spain + IT)
    countries = sorted(df["pais"].dropna().unique().tolist())
    categories = sorted([c for c in df["categoria_tag"].dropna().unique().tolist() if c not in EXCLUDE_CATS])

    default_country = "es" if "es" in countries else (countries[0] if countries else None)
    default_cat = "it-jobs" if "it-jobs" in categories else (categories[0] if categories else None)

    st.session_state.setdefault("country", default_country)
    st.session_state.setdefault("categories", [default_cat] if default_cat else [])
    st.session_state.setdefault("only_salary", False)
    st.session_state.setdefault("contract_type", "All")
    st.session_state.setdefault("contract_time", "All")
    st.session_state.setdefault("search_text", "")
    st.session_state.setdefault("min_salary", None)
    st.session_state.setdefault("max_salary", None)

def sidebar_filters(df: pd.DataFrame):
    st.sidebar.header("Filters")

    countries = sorted(df["pais"].dropna().unique().tolist())
    categories = sorted([c for c in df["categoria_tag"].dropna().unique().tolist() if c not in EXCLUDE_CATS])

    st.session_state["country"] = st.sidebar.selectbox(
        "Country",
        options=countries,
        index=countries.index(st.session_state["country"]) if st.session_state["country"] in countries else 0
    )

    st.session_state["categories"] = st.sidebar.multiselect(
        "Sectors",
        options=categories,
        default=[c for c in st.session_state["categories"] if c in categories] or categories[:1]
    )

    st.session_state["only_salary"] = st.sidebar.checkbox("Only postings with reported salary", value=st.session_state["only_salary"])

    # Contract filters
    contract_types = ["All"] + sorted(df["contract_type"].dropna().astype(str).unique().tolist())
    contract_times = ["All"] + sorted(df["contract_time"].dropna().astype(str).unique().tolist())

    st.session_state["contract_type"] = st.sidebar.selectbox(
        "Contract type", options=contract_types, index=contract_types.index(st.session_state["contract_type"]) if st.session_state["contract_type"] in contract_types else 0
    )
    st.session_state["contract_time"] = st.sidebar.selectbox(
        "Working time", options=contract_times, index=contract_times.index(st.session_state["contract_time"]) if st.session_state["contract_time"] in contract_times else 0
    )

    st.session_state["search_text"] = st.sidebar.text_input("Search (title/description)", value=st.session_state["search_text"])

    st.sidebar.subheader("Salary filter (optional)")
    c1, c2 = st.sidebar.columns(2)
    st.session_state["min_salary"] = c1.number_input("Min", value=st.session_state["min_salary"] or 0, min_value=0, step=1000)
    st.session_state["max_salary"] = c2.number_input("Max", value=st.session_state["max_salary"] or 0, min_value=0, step=1000)

def get_filtered_df(df: pd.DataFrame) -> pd.DataFrame:
    f = df.copy()
    f = f[f["pais"] == st.session_state["country"]]
    if st.session_state["categories"]:
        f = f[f["categoria_tag"].isin(st.session_state["categories"])]

    if st.session_state["contract_type"] != "All":
        f = f[f["contract_type"].astype(str) == st.session_state["contract_type"]]

    if st.session_state["contract_time"] != "All":
        f = f[f["contract_time"].astype(str) == st.session_state["contract_time"]]

    if st.session_state["only_salary"]:
        f = f[f["salary_mid"].notna()]

    # Salary range (if provided)
    min_sal = st.session_state.get("min_salary") or 0
    max_sal = st.session_state.get("max_salary") or 0
    if max_sal > 0:
        f = f[(f["salary_mid"].notna()) & (f["salary_mid"] >= min_sal) & (f["salary_mid"] <= max_sal)]

    # Text search
    q = (st.session_state.get("search_text") or "").strip().lower()
    if q:
        t = (f["title"].fillna("") + " " + f["description"].fillna("")).astype(str).str.lower()
        f = f[t.str.contains(q, regex=False)]

    return f