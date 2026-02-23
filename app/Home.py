import streamlit as st
from utils.data import get_best_available_df, load_master
from utils.theme import inject_theme
inject_theme()

st.set_page_config(page_title="Skill Radar (Adzuna)", layout="wide")

st.title("Skill Radar — Europe (Adzuna)")
st.caption("Dashboard + Personal profile + Projections (built from real job postings).")

df = get_best_available_df()
master = load_master()

c1, c2, c3 = st.columns(3)
c1.metric("Data mode", "MASTER" if not master.empty else "SAMPLE")
c2.metric("Rows loaded", f"{len(df):,}" if not df.empty else "0")
c3.metric("Raw files detected", "Yes" if not df.empty else "No")

st.divider()

st.title("Career Market Intelligence — Prototype v1")

st.markdown("""
### About this prototype

This is the first functional prototype of the Career Market Intelligence application.

The objective of this tool is to help master's and university students better understand the labor market before transitioning into professional life. By analyzing real job postings across Spain (and progressively Europe), the application allows users to explore:

- Which sectors are currently hiring.
- What skills are most demanded.
- Where opportunities are geographically concentrated.
- What salary ranges are associated with specific profiles.

This prototype provides a market overview through interactive filtering and visualization tools. It enables users to explore salary distribution, sector dynamics, and hiring trends in a data-driven way.

---

### Why this tool matters

Many graduates invest time and effort developing skills without clearly understanding:

- Which competencies are best remunerated.
- Which sectors offer stronger salary growth.
- How location impacts compensation.
- What contract types dominate each industry.

This application aims to maximize strategic effort allocation by helping users align their skill development with actual market demand.

---

### Future development (Planned roadmap)

This is an early version and the system is actively under development.

Upcoming improvements include:

- Machine learning models to predict salary ranges based on skills, experience, and sector.
- Predictive analysis of market demand by region and specialization.
- Personalized career simulations.

The long-term vision is to allow users to upload their CV and receive:

- A gap analysis comparing their profile with current market demand.
- Identification of missing or underdeveloped skills.
- Estimated salary improvement potential based on skill upgrades.
- Scenario modeling for career growth over a defined time horizon.

The goal is to transform this tool into a strategic career optimization platform.
""")

if df.empty:
    st.warning(
        "No data found yet in `data/raw/`. Once your download completes and parquet files appear, "
        "this app will populate automatically."
    )