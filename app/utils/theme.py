import streamlit as st

def inject_theme():
    st.markdown("""
    <style>
      /* --- Dark base tweaks (does NOT fight Streamlit theme) --- */
      .stApp {
        background: #0b1220;
      }

      /* Headings */
      h1, h2, h3, h4 {
        color: #e5e7eb !important;
      }

      /* Sidebar */
      section[data-testid="stSidebar"] {
        background: #0f172a !important;
        border-right: 1px solid rgba(255,255,255,0.08);
      }
      section[data-testid="stSidebar"] * {
        color: #e5e7eb !important;
      }

      /* --- Metric cards: dark card + readable text --- */
      div[data-testid="stMetric"] {
        background: #111827 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        padding: 14px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.35) !important;
      }
      div[data-testid="stMetric"] * {
        color: #e5e7eb !important;
      }

      /* Plot container as card */
      .element-container:has(.js-plotly-plot) {
        background: #111827 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        padding: 12px !important;
      }

      /* Dataframe as card */
      .stDataFrame, .stTable {
        background: #111827 !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        overflow: hidden;
      }

      /* Info boxes */
      div[data-testid="stAlert"] {
        border-radius: 14px !important;
      }
    </style>
    """, unsafe_allow_html=True)