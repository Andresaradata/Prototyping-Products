import re
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.data import get_best_available_df
from utils.theme import inject_theme

st.set_page_config(page_title="Overview", layout="wide")
inject_theme()

# ── Load & prepare ─────────────────────────────────────────────────────────────
df_raw = get_best_available_df()
if df_raw.empty:
    st.warning("No data available.")
    st.stop()

df = df_raw.copy()

def _annualize(val):
    if pd.isna(val): return np.nan
    return val * 12 if 800 < val < 8_000 else val

df["salary_min"] = pd.to_numeric(df.get("salary_min"), errors="coerce").apply(_annualize)
df["salary_max"] = pd.to_numeric(df.get("salary_max"), errors="coerce").apply(_annualize)
df["salary_mid"] = df[["salary_min","salary_max"]].mean(axis=1).clip(10_000, 300_000)
df["lat"] = pd.to_numeric(df.get("latitude", pd.Series([""] * len(df))).astype(str).str.replace(",", "."), errors="coerce")
df["lon"] = pd.to_numeric(df.get("longitude", pd.Series([""] * len(df))).astype(str).str.replace(",", "."), errors="coerce")

# ── Sidebar filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="font-size:0.7rem;color:#8b949e;letter-spacing:0.1em;text-transform:uppercase;font-weight:500;padding:1rem 0 0.5rem">Filters</div>', unsafe_allow_html=True)

    countries_all = sorted(df["pais"].dropna().unique().tolist()) if "pais" in df.columns else []
    sel_countries = st.multiselect(
        "Country",
        options=countries_all,
        default=["es"] if "es" in countries_all else countries_all[:1],
    )

    sectors_all = sorted([c for c in df["categoria_tag"].dropna().unique().tolist()
                          if c not in ("unknown","other-general-jobs")]) if "categoria_tag" in df.columns else []
    sel_sectors = st.multiselect("Sector", options=sectors_all, default=[])

    sal_data  = df["salary_mid"].dropna()
    sal_floor = int(sal_data.quantile(0.01)) if len(sal_data) > 0 else 15_000
    sal_ceil  = int(sal_data.quantile(0.99)) if len(sal_data) > 0 else 120_000
    sel_salary = st.slider("Annual salary (€)", min_value=sal_floor, max_value=sal_ceil,
                           value=(sal_floor, sal_ceil), step=2_000, format="€%d")

    sel_text = st.text_input("Search title / company", placeholder="e.g. Python, Madrid…")
    st.divider()
    st.caption("Empty sector = all sectors shown")

# ── Apply filters ──────────────────────────────────────────────────────────────
f = df.copy()
if sel_countries and "pais" in f.columns:
    f = f[f["pais"].isin(sel_countries)]
if sel_sectors and "categoria_tag" in f.columns:
    f = f[f["categoria_tag"].isin(sel_sectors)]

sal_mask = f["salary_mid"].isna() | f["salary_mid"].between(sel_salary[0], sel_salary[1])
f = f[sal_mask]

if sel_text.strip():
    q = sel_text.strip().lower()
    t_hit = f.get("title",   pd.Series([""] * len(f))).fillna("").str.lower().str.contains(q, na=False)
    c_hit = f.get("company", pd.Series([""] * len(f))).fillna("").str.lower().str.contains(q, na=False)
    f = f[t_hit | c_hit]

f = f.reset_index(drop=True)

# ── KPIs ───────────────────────────────────────────────────────────────────────
st.title("Overview — Market Snapshot")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Postings",      f"{len(f):,}")
k2.metric("Sectors",       f"{f['categoria_tag'].nunique():,}" if "categoria_tag" in f.columns else "—")
k3.metric("% with salary", f"{(f['salary_mid'].notna().mean()*100):.1f}%")
k4.metric("Companies",     f"{f['company'].nunique():,}" if "company" in f.columns else "—")

st.divider()

# ── Map ────────────────────────────────────────────────────────────────────────
st.subheader("Job postings map")
m = f.dropna(subset=["lat","lon"])
m = m[m["lat"].between(-90,90) & m["lon"].between(-180,180)].copy()

if m.empty:
    st.warning("No valid coordinates for the current filters.")
else:
    if len(m) > 8000:
        m = m.sample(8000, random_state=42)

    m["_title"]   = m.get("title",            pd.Series(["—"]*len(m))).fillna("—")
    m["_company"] = m.get("company",          pd.Series(["—"]*len(m))).fillna("—")
    m["_loc"]     = m.get("location_display", pd.Series(["—"]*len(m))).fillna("—")
    m["_sector"]  = m.get("sector_label", m.get("categoria_tag", pd.Series(["—"]*len(m)))).fillna("—")
    m["_salary"]  = m["salary_mid"].apply(lambda x: f"€{x:,.0f}" if pd.notna(x) else "Not disclosed")

    fig_map = px.scatter_mapbox(
        m, lat="lat", lon="lon",
        hover_name="_title",
        hover_data={"_company":True,"_loc":True,"_sector":True,"_salary":True,"lat":False,"lon":False},
        color="_sector",
        color_discrete_sequence=px.colors.qualitative.Bold,
        zoom=5, center={"lat":40.2,"lon":-3.7},
        opacity=0.85,
        labels={"_company":"Company","_loc":"Location","_sector":"Sector","_salary":"Salary"},
    )
    fig_map.update_traces(marker=dict(size=7))
    fig_map.update_layout(
        mapbox_style="carto-darkmatter",
        paper_bgcolor="#0d1117",
        margin={"r":0,"t":0,"l":0,"b":0}, height=580,
        legend=dict(bgcolor="rgba(13,17,23,0.85)",bordercolor="#1e2a3a",
                    borderwidth=1,font=dict(color="#c9d1d9",size=12),
                    title=dict(text="Sector",font=dict(color="#8b949e"))),
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption(f"Showing {len(m):,} of {len(f):,} postings · hover for details · scroll to zoom")

st.divider()

# ── Salary by sector ───────────────────────────────────────────────────────────
st.subheader("Median annual salary by sector")
sal_col = "sector_label" if "sector_label" in f.columns else "categoria_tag"
sal_df = (
    f[f["salary_mid"].notna()].groupby(sal_col)["salary_mid"]
    .agg(median="median", count="count")
    .reset_index().query("count >= 5")
    .sort_values("median", ascending=True)
)

if not sal_df.empty:
    fig_sal = go.Figure(go.Bar(
        x=sal_df["median"], y=sal_df[sal_col], orientation="h",
        marker=dict(color=sal_df["median"],
                    colorscale=[[0,"#1e2a3a"],[0.5,"#0a66c2"],[1,"#00b4d8"]],
                    showscale=False),
        text=sal_df["median"].apply(lambda x: f"€{x:,.0f}"),
        textposition="outside", textfont=dict(color="#c9d1d9", size=12),
        hovertemplate="<b>%{y}</b><br>Median: €%{x:,.0f}<extra></extra>",
    ))
    fig_sal.update_layout(
        paper_bgcolor="#0d1117", plot_bgcolor="#0d1117", font_color="#c9d1d9",
        height=max(280, len(sal_df)*42),
        xaxis=dict(gridcolor="#1e2a3a", color="#8b949e", title="Annual Salary (€)"),
        yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c9d1d9"),
        margin=dict(l=10, r=90, t=10, b=10),
    )
    st.plotly_chart(fig_sal, use_container_width=True)
    st.caption(f"Based on {sal_df['count'].sum():,} postings with real salaries")
else:
    st.info("Not enough salary data for current filters.")

st.divider()

# ── Skills in demand ───────────────────────────────────────────────────────────
st.subheader("Skills most in demand")

SKILLS = {
    "Python":              ["python","pandas","numpy","fastapi","django","flask"],
    "JavaScript / TS":     ["javascript","typescript","node.js","react","angular","vue"],
    "Java":                ["java","spring","hibernate"],
    "SQL / Databases":     ["sql","mysql","postgresql","postgres","oracle","mongodb"],
    "Cloud (AWS/Azure/GCP)":["aws","azure","gcp","cloud"],
    "DevOps / Docker":     ["docker","kubernetes","terraform","ci/cd","jenkins","devops"],
    "ML / AI":             ["machine learning","deep learning","tensorflow","pytorch","llm","gpt","nlp"],
    "Data Engineering":    ["spark","kafka","airflow","databricks","dbt","etl"],
    "SAP / ERP":           ["sap","abap","erp","fiori"],
    "Cybersecurity":       ["cybersecurity","ciberseguridad","soc","siem","pentesting"],
    "Excel / BI":          ["excel","power bi","tableau","looker","qlik"],
    "Agile / Scrum":       ["agile","scrum","kanban","sprint"],
    "React / Frontend":    ["react","vue","angular","next.js","frontend"],
    "C++ / Embedded":      ["c++","embedded","firmware","rtos","fpga"],
}

text_blob = (
    f.get("title",       pd.Series([""] * len(f))).fillna("") + " " +
    f.get("description", pd.Series([""] * len(f))).fillna("")
).str.lower()

n_total = max(len(f), 1)
rows = []
for name, patterns in SKILLS.items():
    rx    = "|".join(re.escape(p) for p in patterns)
    count = int(text_blob.str.contains(rx, na=False).sum())
    if count > 0:
        rows.append({"skill": name, "count": count, "pct": round(count / n_total * 100, 1)})

skill_df = pd.DataFrame(rows).sort_values("count", ascending=True)

if not skill_df.empty:
    col_l, col_r = st.columns([3, 1])

    with col_l:
        fig_sk = px.bar(
            skill_df, x="pct", y="skill", orientation="h",
            labels={"pct":"% of job listings","skill":""},
            color="pct",
            color_continuous_scale=[[0,"#1e2a3a"],[0.5,"#0a66c2"],[1,"#00b4d8"]],
            text=skill_df["pct"].apply(lambda x: f"{x:.1f}%"),
        )
        fig_sk.update_traces(textposition="outside", textfont=dict(color="#c9d1d9", size=11))
        fig_sk.update_layout(
            paper_bgcolor="#0d1117", plot_bgcolor="#0d1117", font_color="#c9d1d9",
            height=max(340, len(skill_df)*34),
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#1e2a3a", color="#8b949e"),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", color="#c9d1d9"),
            margin=dict(l=10, r=70, t=10, b=10),
        )
        st.plotly_chart(fig_sk, use_container_width=True)

    with col_r:
        st.markdown("<br><br>", unsafe_allow_html=True)
        for _, row in skill_df.sort_values("count", ascending=False).head(5).iterrows():
            st.markdown(f"""
<div style="background:#161b27;border:1px solid #1e2a3a;border-radius:8px;
padding:0.6rem 0.9rem;margin-bottom:0.5rem">
<div style="font-size:0.8rem;font-weight:600;color:#e6edf3">{row['skill']}</div>
<div style="font-size:0.72rem;color:#0a66c2;margin-top:2px">{row['count']:,} listings · {row['pct']}%</div>
</div>""", unsafe_allow_html=True)

    st.caption(f"Extracted from job titles and descriptions · {n_total:,} postings analysed")
else:
    st.info("No skill data for current filters.")
