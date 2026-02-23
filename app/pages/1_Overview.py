import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

from utils.data import get_best_available_df
from utils.filters import init_filters, sidebar_filters, get_filtered_df
from utils.theme import inject_theme

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(page_title="Overview", layout="wide")
inject_theme()

def safe_str(x):
    return x if isinstance(x, str) and x.strip() else "—"

# --------------------------------------------------
# Load data
# --------------------------------------------------
df = get_best_available_df()

if df.empty:
    st.warning("No data available.")
    st.stop()

df = df.copy()

df["salary_min"] = pd.to_numeric(df.get("salary_min"), errors="coerce")
df["salary_max"] = pd.to_numeric(df.get("salary_max"), errors="coerce")

df["salary_mid"] = (df["salary_min"] + df["salary_max"]) / 2

# --------------------------------------------------
# Filters
# --------------------------------------------------
init_filters(df)
sidebar_filters(df)
f = get_filtered_df(df)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.title("Overview — Market Snapshot")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Postings", f"{len(f):,}")
k2.metric("Sectors", f"{f['categoria_tag'].nunique():,}" if "categoria_tag" in f.columns else "—")
k3.metric("% with salary", f"{(f['salary_mid'].notna().mean() * 100):.1f}%")
k4.metric("Companies", f"{f['company'].nunique():,}" if "company" in f.columns else "—")

st.divider()

# --------------------------------------------------
# Prepare coordinates
# --------------------------------------------------
required_cols = ["latitude", "longitude"]

if not all(col in f.columns for col in required_cols):
    st.error("Latitude/Longitude columns not found in dataset.")
    st.stop()

m = f.copy()

m["lat"] = pd.to_numeric(
    m["latitude"].astype(str).str.replace(",", ".", regex=False),
    errors="coerce"
)

m["lon"] = pd.to_numeric(
    m["longitude"].astype(str).str.replace(",", ".", regex=False),
    errors="coerce"
)

m = m.dropna(subset=["lat", "lon"])
m = m[m["lat"].between(-90, 90) & m["lon"].between(-180, 180)].reset_index(drop=True)

if m.empty:
    st.warning("No valid coordinates for current filters.")
    st.stop()

# Limit for performance
if len(m) > 6000:
    m = m.sample(6000, random_state=42).reset_index(drop=True)

# Ensure display column exists
if "location_display" not in m.columns:
    m["location_display"] = "—"

# --------------------------------------------------
# Create Map
# --------------------------------------------------
center_lat = float(m["lat"].median())
center_lon = float(m["lon"].median())

folium_map = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=5,
    tiles="CartoDB dark_matter",
    control_scale=True,
)

for _, row in m.iterrows():
    title = safe_str(row.get("title"))
    company = safe_str(row.get("company"))
    location = safe_str(row.get("location_display"))

    sal_min = row.get("salary_min")
    sal_max = row.get("salary_max")

    if pd.notna(sal_min) or pd.notna(sal_max):
        salary_text = f"{sal_min if pd.notna(sal_min) else '—'} – {sal_max if pd.notna(sal_max) else '—'}"
    else:
        salary_text = "Not disclosed"

    popup_html = f"""
    <b>{title}</b><br/>
    {company}<br/>
    {location}<br/>
    <b>Salary:</b> {salary_text}
    """

    folium.CircleMarker(
        location=(float(row["lat"]), float(row["lon"])),
        radius=6,
        color="#10b981",
        fill=True,
        fill_color="#10b981",
        fill_opacity=0.85,
        weight=1,
        popup=popup_html,
    ).add_to(folium_map)

st.subheader("Map")
st_folium(folium_map, use_container_width=True, height=650)