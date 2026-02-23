import streamlit as st
import pandas as pd
from utils.data import get_best_available_df
from utils.theme import inject_theme
inject_theme()

st.title("Profile & salary — Individual insights")

df = get_best_available_df()
if df.empty:
    st.warning("No data available yet.")
    st.stop()

df = df.copy()
df["salary_mid"] = (pd.to_numeric(df.get("salary_min"), errors="coerce") + pd.to_numeric(df.get("salary_max"), errors="coerce")) / 2

countries = sorted(df["pais"].dropna().unique().tolist())
categories = sorted([c for c in df["categoria_tag"].dropna().unique().tolist() if c not in ("unknown", "other-general-jobs")])

with st.form("profile_form"):
    c1, c2 = st.columns(2)
    country = c1.selectbox("Target country", options=countries, index=countries.index("es") if "es" in countries else 0)
    sector = c2.selectbox("Sector (category)", options=categories, index=categories.index("it-jobs") if "it-jobs" in categories else 0)

    target_role = st.text_input("Target role (e.g., Data Analyst, BI Consultant, ML Engineer)", value="Data Analyst")
    level = st.selectbox("Level", ["Junior", "Mid", "Senior"])
    interested_remote = st.checkbox("Interested in remote/hybrid", value=True)

    submitted = st.form_submit_button("Get insights")

if not submitted:
    st.stop()

f = df[(df["pais"] == country) & (df["categoria_tag"] == sector)].copy()

st.subheader("Salary estimate (from postings with reported salary)")

sal = f.dropna(subset=["salary_mid"])["salary_mid"]

if len(sal) >= 30:
    p25, p50, p75 = sal.quantile([0.25, 0.50, 0.75]).tolist()
    st.write(f"Suggested range (P25–P75): **{p25:,.0f} – {p75:,.0f}**")
    st.write(f"Median (P50): **{p50:,.0f}**")
    st.caption("This is an empirical benchmark from posted salary data, not a guaranteed offer.")
else:
    st.warning("Not enough salary postings for this country-sector. Falling back to a country-level benchmark.")
    sal2 = df[(df["pais"] == country)].dropna(subset=["salary_mid"])["salary_mid"]
    if len(sal2) >= 30:
        p25, p50, p75 = sal2.quantile([0.25, 0.50, 0.75]).tolist()
        st.write(f"Country benchmark (P25–P75): **{p25:,.0f} – {p75:,.0f}** | Median: **{p50:,.0f}**")
    else:
        st.error("Still not enough salary data in the current dataset. This will improve as more data is downloaded.")

st.divider()
st.subheader("Operational insights")

st.write(f"Available postings for this country-sector: **{len(f):,}**")

# Contract types (if present)
if "contract_type" in f.columns and f["contract_type"].notna().any():
    top_contract = f["contract_type"].dropna().value_counts().head(5)
    st.write("Most common contract types:")
    st.dataframe(top_contract)

# Contract time (if present)
if "contract_time" in f.columns and f["contract_time"].notna().any():
    top_time = f["contract_time"].dropna().value_counts().head(5)
    st.write("Most common working time:")
    st.dataframe(top_time)

# Remote heuristic
if interested_remote:
    text = (f.get("title", "").fillna("") + " " + f.get("description", "").fillna("")).astype(str).str.lower()
    remote_share = text.str.contains("remote|remoto|teletrabajo|hybrid|híbrido|work from home|wfh").mean()
    st.write(f"Remote/hybrid signal (text heuristic): **{remote_share*100:.1f}%**")

st.info("Next step (once we extract skills): skill-gap insights vs. market and recommended skill bundles.")