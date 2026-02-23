import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from utils.data import get_best_available_df
from utils.theme import inject_theme
inject_theme()

st.title("Projections — Sector demand (skills coming next)")

df = get_best_available_df()
if df.empty:
    st.warning("No data available yet.")
    st.stop()

df = df.copy()

# Ensure quarter exists
if "trimestre" not in df.columns and "created" in df.columns:
    dt = pd.to_datetime(df["created"], errors="coerce", utc=True)
    q = ((dt.dt.month - 1) // 3 + 1).astype("Int64")
    df["trimestre"] = dt.dt.year.astype("Int64").astype(str) + "-Q" + q.astype(str)

df = df.dropna(subset=["pais", "categoria_tag", "trimestre"])
df = df[~df["categoria_tag"].isin(["unknown", "other-general-jobs"])]

countries = sorted(df["pais"].unique().tolist())
categories = sorted(df["categoria_tag"].unique().tolist())

c1, c2 = st.columns(2)
country = c1.selectbox("Country", options=countries, index=countries.index("es") if "es" in countries else 0)
sector = c2.selectbox("Sector (category)", options=categories, index=categories.index("it-jobs") if "it-jobs" in categories else 0)

f = df[(df["pais"] == country) & (df["categoria_tag"] == sector)].copy()

# Quarterly counts
g = f.groupby("trimestre", as_index=False).size().rename(columns={"size": "postings"}).sort_values("trimestre")

st.subheader("Time series (posting counts by quarter)")
fig = px.line(g, x="trimestre", y="postings", markers=True)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Simple projection (explainable)")
if len(g) >= 4:
    g = g.reset_index(drop=True)
    g["t"] = range(len(g))
    X = g[["t"]].values
    y = g["postings"].values

    model = LinearRegression().fit(X, y)

    horizon = 4  # next 4 quarters
    future = pd.DataFrame({"t": range(len(g), len(g) + horizon)})
    yhat = model.predict(future[["t"]].values)

    out = pd.concat(
        [
            g[["trimestre", "postings"]],
            pd.DataFrame({"trimestre": [f"FUT+{i+1}" for i in range(horizon)], "postings": yhat}),
        ],
        ignore_index=True,
    )

    fig2 = px.line(out, x="trimestre", y="postings", markers=True, title="Historical + projected (next 4 quarters)")
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Model: simple linear regression over time index (high explainability; refined later with more history).")
else:
    st.info("Not enough quarters yet to project. This will improve as your dataset grows (2 years = 8 quarters).")

st.divider()
st.subheader("Skills (coming next)")
st.write(
    "Once we run the skills extractor on `title + description`, this page will show: "
    "top skills by quarter, emerging skills, and skill bundles per target role."
)