import streamlit as st
import pandas as pd
from utils.data import get_best_available_df
from utils.theme import inject_theme

st.set_page_config(page_title="Career Market Intelligence", layout="wide")
inject_theme()

df = get_best_available_df()

# ── KPIs from data ────────────────────────────────────────────────────────────
total_rows      = len(df) if not df.empty else 0
total_sectors   = df["categoria_tag"].nunique() if not df.empty and "categoria_tag" in df.columns else 0
total_companies = df["company"].nunique() if not df.empty and "company" in df.columns else 0
pct_salary      = (
    pd.to_numeric(df.get("salary_min"), errors="coerce").notna().mean() * 100
    if not df.empty else 0
)

# ══════════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="padding:2.5rem 0 1.5rem">
    <div style="font-size:0.72rem;color:#0a66c2;font-weight:600;
                letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.75rem">
        ESADE · Prototyping Products 2026 · v2
    </div>
    <h1 style="font-size:3rem !important;border:none !important;padding:0 !important;
               letter-spacing:-0.04em;line-height:1.1;margin-bottom:1rem">
        Career Market<br/>Intelligence
    </h1>
    <p style="font-size:1.15rem;color:#8b949e;max-width:580px;margin:0;line-height:1.7">
        A data-driven tool that helps students understand the Spanish job market
        before entering professional life — built from real job postings and
        validated against official government statistics.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Live data stats ───────────────────────────────────────────────────────────
st.markdown("""
<div style="display:flex;gap:2rem;padding:1.25rem 0 2rem;flex-wrap:wrap">
""" + "".join([
    f"""<div style="border-left:2px solid #0a66c2;padding-left:1rem">
        <div style="font-size:1.6rem;font-weight:700;color:#e6edf3;letter-spacing:-0.02em">{val}</div>
        <div style="font-size:0.75rem;color:#8b949e;font-weight:500;text-transform:uppercase;
                    letter-spacing:0.06em;margin-top:2px">{label}</div>
    </div>"""
    for label, val in [
        ("job postings", f"{total_rows:,}"),
        ("sectors covered", str(total_sectors)),
        ("companies", f"{total_companies:,}"),
        ("with real salary", f"{pct_salary:.0f}%"),
    ]
]) + "</div>", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# NAVIGATION CARDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div style="font-size:0.72rem;color:#8b949e;font-weight:500;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:1rem">Navigate the app</div>', unsafe_allow_html=True)

nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    st.markdown("""
<div style="background:linear-gradient(135deg,#0d1f3c 0%,#0a1628 100%);
border:1px solid #0a66c2;border-radius:14px;padding:1.5rem 1.75rem">
    <div style="font-size:1.5rem;margin-bottom:0.5rem">🗺️</div>
    <div style="font-size:1rem;font-weight:600;color:#e6edf3;margin-bottom:0.5rem">
        Page 1 · Overview
    </div>
    <div style="font-size:0.85rem;color:#8b949e;line-height:1.6;margin-bottom:1rem">
        Explore the market. Interactive map of all job postings across Spain,
        filterable by sector, salary, and keyword. See which skills appear most
        in listings and how salaries compare across sectors.
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:0.5rem">
        <span style="background:#1e2a3a;color:#8b949e;border-radius:4px;
                     padding:2px 10px;font-size:0.72rem">Interactive map</span>
        <span style="background:#1e2a3a;color:#8b949e;border-radius:4px;
                     padding:2px 10px;font-size:0.72rem">Live filters</span>
        <span style="background:#1e2a3a;color:#8b949e;border-radius:4px;
                     padding:2px 10px;font-size:0.72rem">Skills ranking</span>
    </div>
</div>
""", unsafe_allow_html=True)
    st.page_link("pages/1_Overview.py", label="Open Overview →", use_container_width=True)

with nav_col2:
    st.markdown("""
<div style="background:linear-gradient(135deg,#161b27 0%,#111827 100%);
border:1px solid #1e2a3a;border-radius:14px;padding:1.5rem 1.75rem">
    <div style="font-size:1.5rem;margin-bottom:0.5rem">📊</div>
    <div style="font-size:1rem;font-weight:600;color:#e6edf3;margin-bottom:0.5rem">
        Page 2 · ML &amp; Projections
    </div>
    <div style="font-size:0.85rem;color:#8b949e;line-height:1.6;margin-bottom:1rem">
        Estimate your salary. Select a role and skills to get a prediction
        anchored to official INE 2023 data. See where those jobs concentrate
        in Spain and how market salaries have evolved since 2015.
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:0.5rem">
        <span style="background:#1e2a3a;color:#8b949e;border-radius:4px;
                     padding:2px 10px;font-size:0.72rem">Salary estimator</span>
        <span style="background:#1e2a3a;color:#8b949e;border-radius:4px;
                     padding:2px 10px;font-size:0.72rem">Spain heatmap</span>
        <span style="background:#1e2a3a;color:#8b949e;border-radius:4px;
                     padding:2px 10px;font-size:0.72rem">INE projections</span>
    </div>
</div>
""", unsafe_allow_html=True)
    st.page_link("pages/2_ML_and_Projections.py", label="Open ML & Projections →", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# METHODOLOGY — two columns
# ══════════════════════════════════════════════════════════════════════════════
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("### How the salary estimator works")
    st.markdown("""
Training a machine learning model directly on job posting salaries produces unreliable results
in this dataset — only **18.8% of listings** include a real employer-posted salary, and the rest
are Adzuna API estimates that introduce noise.

Instead the estimator uses a **transparent, auditable formula** grounded entirely in official
government data:
""")

    for step, title, detail in [
        ("1", "Base salary", "INE EAES 2023 — official sector average by CNAE code"),
        ("2", "Seniority adjustment", "Intern 0.55× · Junior 0.72× · Mid 1.0× · Senior 1.38× · Manager 1.75×"),
        ("3", "Skill premiums", "Each skill adds 3–12% on top (ML/AI +12%, Cloud +9%, DevOps +8%…)"),
        ("4", "Remote premium", "+8% for remote or hybrid roles"),
        ("5", "Uncertainty range", "±15–22% band based on INE salary distribution spread"),
    ]:
        st.markdown(f"""
<div style="display:flex;gap:1rem;align-items:flex-start;margin-bottom:0.75rem">
    <div style="min-width:28px;height:28px;background:#0a66c2;border-radius:50%;
                display:flex;align-items:center;justify-content:center;
                font-size:0.75rem;font-weight:700;color:#fff;flex-shrink:0;margin-top:2px">
        {step}
    </div>
    <div>
        <div style="font-size:0.9rem;font-weight:600;color:#e6edf3">{title}</div>
        <div style="font-size:0.82rem;color:#8b949e;line-height:1.5">{detail}</div>
    </div>
</div>
""", unsafe_allow_html=True)

with right:
    st.markdown("### Data sources")

    for icon, name, detail, url in [
        ("📋", "Adzuna Jobs API", "~12,000 real job postings across Spain · 10 sectors · 2024–2025", "https://developer.adzuna.com/"),
        ("🏛️", "INE EAES 2023", "Encuesta Anual de Estructura Salarial · Official annual salaries by CNAE sector · Published 28/05/2025", "https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177025"),
        ("📊", "SEPE Datos Abiertos", "Contratos Registrados por Municipio · Contract volumes by sector 2015–2024", "https://sede.sepe.gob.es/portalSede/en/datos-abiertos/catalogo-de-datos-del-SEPE"),
        ("📚", "Hays & Michael Page Spain", "Skill salary premiums · Spain Salary Guides 2024", ""),
    ]:
        st.markdown(f"""
<div style="background:#161b27;border:1px solid #1e2a3a;border-radius:10px;
padding:0.9rem 1.1rem;margin-bottom:0.6rem">
    <div style="font-size:0.88rem;font-weight:600;color:#e6edf3;margin-bottom:3px">
        {icon} &nbsp;{name}
    </div>
    <div style="font-size:0.79rem;color:#8b949e;line-height:1.5">{detail}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### What changed from v1")

    changes = [
        ("All 10 Spain sectors", "was IT only"),
        ("Live map filters", "map was static"),
        ("INE-anchored estimator", "no salary model"),
        ("Official INE + SEPE projections", "sparse Adzuna trends"),
        ("Salary data cleaned", "raw predicted salaries mixed in"),
    ]
    for new, old in changes:
        st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
padding:0.4rem 0;border-bottom:1px solid #1e2a3a">
    <span style="font-size:0.83rem;color:#e6edf3">✓ &nbsp;{new}</span>
    <span style="font-size:0.76rem;color:#8b949e;font-style:italic">{old}</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### Planned for v3")

road_cols = st.columns(3)
roadmap = [
    ("📄", "CV upload", "Upload your CV and get an automatic skill gap analysis compared to live market demand"),
    ("📈", "Salary simulator", "See how learning a new skill or getting a certification would change your estimated salary"),
    ("🔮", "Advanced forecasting", "Replace linear regression with ARIMA / Prophet on SEPE monthly contract data for more reliable projections"),
]
for col, (icon, title, desc) in zip(road_cols, roadmap):
    with col:
        st.markdown(f"""
<div style="background:#161b27;border:1px solid #1e2a3a;border-radius:10px;
padding:1rem 1.1rem;height:100%">
    <div style="font-size:1.2rem;margin-bottom:6px">{icon}</div>
    <div style="font-size:0.88rem;font-weight:600;color:#c9d1d9;margin-bottom:4px">{title}</div>
    <div style="font-size:0.8rem;color:#8b949e;line-height:1.5">{desc}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if df.empty:
    st.warning("No data found in `data/raw/`. Make sure your parquet files are there and restart the app.")
