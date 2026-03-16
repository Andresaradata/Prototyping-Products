import streamlit as st

def inject_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'IBM Plex Sans', sans-serif !important;
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
    }
    .main .block-container {
        padding: 2rem 2.5rem 3rem;
        max-width: 1200px;
    }
    section[data-testid="stSidebar"] {
        background-color: #0a0f1e !important;
        border-right: 1px solid #1e2a3a;
    }
    section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }

    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #161b27 0%, #111827 100%);
        border: 1px solid #1e2a3a;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        transition: border-color 0.2s;
    }
    div[data-testid="metric-container"]:hover { border-color: #0a66c2; }
    div[data-testid="metric-container"] label {
        color: #8b949e !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] [data-testid="metric-value"] {
        color: #e6edf3 !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em;
    }

    h1 {
        color: #e6edf3 !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
        letter-spacing: -0.02em;
        border-left: 3px solid #0a66c2;
        padding-left: 0.75rem;
        margin-bottom: 0.25rem !important;
    }
    h2, h3 { color: #c9d1d9 !important; font-weight: 500 !important; }
    hr { border-color: #1e2a3a !important; }

    /* Pre-selected multiselect tags = LinkedIn blue */
    span[data-baseweb="tag"] {
        background-color: #0a66c2 !important;
        border-radius: 4px !important;
        color: #ffffff !important;
    }
    span[data-baseweb="tag"] span { color: #ffffff !important; }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #161b27 !important;
        border-color: #1e2a3a !important;
        border-radius: 8px !important;
        color: #e6edf3 !important;
    }
    div[data-baseweb="select"] > div:focus-within,
    div[data-baseweb="input"] > div:focus-within {
        border-color: #0a66c2 !important;
        box-shadow: 0 0 0 2px rgba(10,102,194,0.2) !important;
    }

    div[data-testid="stSlider"] div[role="slider"] { background-color: #0a66c2 !important; }

    .stButton > button {
        background: #0a66c2 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 24px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: #004182 !important;
        box-shadow: 0 4px 16px rgba(10,102,194,0.4) !important;
    }
    .stFormSubmitButton > button {
        background: #0a66c2 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 24px !important;
        font-weight: 600 !important;
        padding: 0.6rem 2rem !important;
        transition: all 0.2s ease !important;
    }
    .stFormSubmitButton > button:hover {
        background: #004182 !important;
        box-shadow: 0 4px 16px rgba(10,102,194,0.4) !important;
    }

    .stDataFrame {
        border-radius: 10px !important;
        border: 1px solid #1e2a3a !important;
        overflow: hidden;
    }

    div[data-testid="stInfo"] {
        background: rgba(10,102,194,0.08) !important;
        border-left: 3px solid #0a66c2 !important;
        border-radius: 0 8px 8px 0 !important;
    }
    div[data-testid="stSuccess"] {
        background: rgba(0,200,130,0.08) !important;
        border-left: 3px solid #00c882 !important;
        border-radius: 0 8px 8px 0 !important;
    }
    div[data-testid="stWarning"] {
        background: rgba(255,180,0,0.08) !important;
        border-left: 3px solid #ffb400 !important;
        border-radius: 0 8px 8px 0 !important;
    }

    .stCaption, small { color: #8b949e !important; }

    textarea {
        background-color: #161b27 !important;
        border-color: #1e2a3a !important;
        color: #e6edf3 !important;
        border-radius: 8px !important;
    }
    textarea:focus {
        border-color: #0a66c2 !important;
        box-shadow: 0 0 0 2px rgba(10,102,194,0.2) !important;
    }

    .stDownloadButton > button {
        background: transparent !important;
        color: #0a66c2 !important;
        border: 1px solid #0a66c2 !important;
        border-radius: 24px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    .stDownloadButton > button:hover { background: rgba(10,102,194,0.1) !important; }

    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #1e2a3a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #0a66c2; }
    </style>
    """, unsafe_allow_html=True)
