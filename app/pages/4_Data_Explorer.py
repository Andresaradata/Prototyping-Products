import streamlit as st
import pandas as pd

from utils.data import get_best_available_df
from utils.filters import init_filters, sidebar_filters, get_filtered_df
from utils.theme import inject_theme

st.set_page_config(page_title="Data Explorer", layout="wide")
inject_theme()

df = get_best_available_df()
if df.empty:
    st.warning("No data available yet.")
    st.stop()

df = df.copy()
df["salary_mid"] = (pd.to_numeric(df.get("salary_min"), errors="coerce") + pd.to_numeric(df.get("salary_max"), errors="coerce")) / 2

init_filters(df)
sidebar_filters(df)

f = get_filtered_df(df)

st.title("Data Explorer")
st.caption("Inspect the dataset with global filters (country, sector, contract, salary, text search).")

c1, c2, c3 = st.columns(3)
limit = c1.selectbox("Rows to display", options=[100, 500, 1000, 5000], index=1)
sort_col = c2.selectbox("Sort by", options=[c for c in f.columns if c in ("created","salary_mid","company","location_display","categoria_tag")] + list(f.columns))
sort_dir = c3.selectbox("Direction", options=["Descending", "Ascending"], index=0)

ff = f.sort_values(sort_col, ascending=(sort_dir == "Ascending")) if sort_col in f.columns else f
st.dataframe(ff.head(limit), use_container_width=True, height=650)

st.download_button(
    "Download filtered data (CSV)",
    data=ff.to_csv(index=False).encode("utf-8"),
    file_name="filtered_postings.csv",
    mime="text/csv"
)