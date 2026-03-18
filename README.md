<div align="center">

# 💼 Career Market Intelligence
### *Spain Labour Market Dashboard — Prototype v2*

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=flat-square&logo=plotly&logoColor=white)
![Data: Adzuna](https://img.shields.io/badge/Data-Adzuna%20API-0A66C2?style=flat-square)
![Data: INE](https://img.shields.io/badge/Official-INE%20%26%20SEPE-006400?style=flat-square)
![ESADE](https://img.shields.io/badge/ESADE-Prototyping%202026-8B0000?style=flat-square)

**A data-driven tool to help students understand the Spanish job market before entering professional life.**
Built from ~12,000 real job postings · validated against official INE & SEPE government statistics · 3-page interactive Streamlit app.

[🚀 Run locally](#-getting-started) · [📊 Data sources](#-data-sources) · [🤖 How the model works](#-salary-estimator) · [📈 What changed from v1](#-v1--v2-changes)

---

</div>

## 🎯 What this tool does

Most graduates enter the job market without knowing which skills are valued, where salaries are higher, or what roles are in demand. This app answers those questions with real data.

| Question | Where to find it |
|----------|-----------------|
| Where are the jobs in Spain? | **Page 1** — interactive Plotly map, filterable by sector & salary |
| Which skills are most demanded? | **Page 1** — ranked chart extracted from job descriptions |
| What salary should I expect? | **Page 2** — estimator anchored to official INE 2023 data |
| Where are jobs concentrated geographically? | **Page 2** — Spain density heatmap per sector |
| Is demand growing or shrinking? | **Page 2** — INE + SEPE official time-series with forecast |

---

## 🗺️ App overview

### 🏠 Home
Project documentation, methodology explained, data sources, and what changed from v1 to v2.

### 📊 Page 1 · Overview — *"Show me the market"*

- **Interactive job map** — ~12,000 postings across Spain, coloured by sector, hover for salary & company details
- **Live sidebar filters** — country, sector, salary range, text search — every chart updates in real time
- **Median salary by sector** — ranked horizontal bar chart with sample sizes
- **Skills in demand** — 14 skill groups extracted from job titles and descriptions, shown as % of listings

### 🤖 Page 2 · ML & Projections — *"What will I earn, and where?"*

- **Salary estimator** — select from 35 curated job titles, tick relevant skills, get an estimate in seconds
- **Spain job density heatmap** — bubbles showing geographic concentration per ~10km zone
- **Salary distribution** — histogram from real postings with your estimate and INE benchmark marked
- **INE salary evolution 2015–2027** — official annual data with linear regression forecast per sector
- **SEPE contract demand** — registered contracts by broad sector showing the full 2020 COVID drop and recovery

---

## 🚀 Getting started

```bash
# 1. Clone the repo
git clone https://github.com/Andresaradata/Prototyping-Products.git
cd Prototyping-Products/Iteration_2

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch
python -m streamlit run app/Home.py
```

> ⚠️ **Always run from `Iteration_2/`** — the app resolves `data/raw/` relative to where the command is run.

---

## 📁 Project structure

```
Iteration_2/
├── app/
│   ├── Home.py                      ← Landing page & documentation
│   ├── pages/
│   │   ├── 1_Overview.py            ← Map + skills + salary by sector
│   │   └── 2_ML_and_Projections.py  ← Estimator + heatmap + projections
│   └── utils/
│       ├── data.py                  ← Auto-merges all Spain sector files
│       ├── filters.py               ← Sidebar filter logic
│       └── theme.py                 ← LinkedIn-style dark theme (IBM Plex Sans)
├── data/
│   └── raw/
│       └── anuncios_es_*.parquet    ← Adzuna data — 10 Spain sectors
└── requirements.txt
```

---

## 📊 Data sources

### Job postings — Adzuna API

Raw listings collected from the [Adzuna Jobs API](https://developer.adzuna.com/) for Spain across 10 sectors.

| Sector | File |
|--------|------|
| IT & Technology | `anuncios_es_it-jobs.parquet` |
| Engineering | `anuncios_es_engineering-jobs.parquet` |
| Accounting & Finance | `anuncios_es_accounting-finance-jobs.parquet` |
| Healthcare & Nursing | `anuncios_es_healthcare-nursing-jobs.parquet` |
| Hospitality & Catering | `anuncios_es_hospitality-catering-jobs.parquet` |
| Logistics & Warehouse | `anuncios_es_logistics-warehouse-jobs.parquet` |
| Manufacturing | `anuncios_es_manufacturing-jobs.parquet` |
| Sales | `anuncios_es_sales-jobs.parquet` |
| Teaching & Education | `anuncios_es_teaching-jobs.parquet` |
| Trade & Construction | `anuncios_es_trade-construction-jobs.parquet` |

> **Known data limitation:** Only ~18.8% of listings include a real employer-posted salary.  
> Adzuna fills the rest with API estimates and flags them as `salary_is_predicted = True`.  
> These rows are **excluded from all salary analysis** — we only use actual posted salaries.

### Official statistics — INE & SEPE

| Source | Dataset | Period | Used for |
|--------|---------|--------|----------|
| [INE EAES](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177025) | Encuesta Anual de Estructura Salarial | 2015–2023 | Sector salary benchmarks, seniority multipliers |
| [SEPE Datos Abiertos](https://sede.sepe.gob.es/portalSede/en/datos-abiertos/catalogo-de-datos-del-SEPE) | Contratos Registrados por Municipio | 2015–2024 | Contract volume and sector demand trends |

INE EAES 2023 definitive data published **28/05/2025** · Spain national average: **€28,049/year**

---

## 🤖 Salary estimator

### Why not a pure ML model?

We tested a Gradient Boosting Regressor on Adzuna salary data. The problem: with only ~2,300 usable training rows (real salary, valid features), the model learned backwards — more skills predicted *lower* salary; senior roles predicted less than junior. This is a well-known issue with sparse, non-representative training data and impossible to fix by tuning.

### The approach: INE-anchored transparent calculator

A 5-step formula fully traceable to public data — no black box.

```
Step 1  Base      = INE EAES 2023 official sector average (by CNAE code)
Step 2  Seniority = Base × multiplier
Step 3  Skills    = Seniority-adjusted × (1 + Σ skill premiums)  [capped at +35%]
Step 4  Remote    = Skills-adjusted × 1.08  (if remote / hybrid)
Step 5  Range     = Final ± 15–22%  (based on INE salary distribution spread)
```

---

## 📈 v1 → v2 changes

| Area | v1 | v2 |
|------|----|----|
| Pages | 4 fragmented pages | 3 focused pages |
| Data scope | IT jobs only | All 10 Spain sectors merged |
| Map | Folium (broken render) | Plotly Mapbox (interactive, reliable) |
| Sidebar filters | Didn't affect charts | All charts update in real time |
| Salary data | Raw values, no cleaning | Monthly→annual detection, outlier capping |
| Salary prediction | Not implemented | INE-anchored transparent calculator |
| Projections | Adzuna trends (too sparse) | Official INE EAES + SEPE 2015–2024 data |
| Design | Basic | LinkedIn-style dark theme (IBM Plex Sans) |

---

## 🔭 Roadmap — v3

- [ ] CV upload → automatic skill gap analysis vs. live market demand
- [ ] Skill-to-salary improvement simulator ("if I learn cloud, +€X/year")
- [ ] Regional breakdown by Comunidad Autónoma
- [ ] ARIMA / Prophet forecasting on SEPE monthly contract data
- [ ] Personalised career path recommendations

---

## 🔧 Requirements

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.24.0
pyarrow>=14.0.0
plotly>=5.18.0
scikit-learn>=1.3.0
```

---

<div align="center">

Built at **ESADE · Prototyping Products 2026**

*Data: [Adzuna API](https://developer.adzuna.com/) · [INE EAES](https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177025) · [SEPE datos abiertos](https://sede.sepe.gob.es/portalSede/en/datos-abiertos/catalogo-de-datos-del-SEPE)*

</div>
