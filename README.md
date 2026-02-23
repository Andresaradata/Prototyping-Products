## Career Market Intelligence — Prototype v1
Overview
####  FOR USE python -m streamlit run app/Home.py
Career Market Intelligence is an early-stage prototype designed to analyze labor market dynamics across Spain and progressively Europe.

This application helps students and early-career professionals understand:

Which sectors are currently hiring

What skills are most demanded

How salary ranges vary by industry and location

Where opportunities are geographically concentrated

The objective of this tool is to provide data-driven visibility into real job market conditions and support more strategic career decision-making.

Purpose of this Prototype

This first version focuses on market exploration and visualization.

Users can:

Filter job postings by country, sector, contract type and salary range

Visualize job concentration geographically

Inspect salary ranges directly within the interactive map

Explore high-level market indicators

This version represents the foundation of a broader career intelligence system currently under development.

Future Vision

The long-term objective is to evolve this prototype into a personalized career optimization platform powered by machine learning.

Planned developments include:

Salary prediction models based on skills, experience and sector

Demand forecasting by region and specialization

CV upload and automatic skill gap analysis

Salary improvement simulations based on skill acquisition

Career growth modeling over time

The final goal is to help users align their professional development with real market demand and maximize long-term income potential.

Current Features (Prototype v1)

Interactive market overview dashboard

Geographic job visualization

Salary visibility within map popups

Sector and contract filtering

Salary range filtering

Data exploration module

Project Structure

app/
├── Home.py
├── main.py
├── pages/
│ ├── 1_Overview.py
│ ├── 2_Profile_and_Salary.py
│ ├── 3_Projections.py
│ └── 4_Data_Explorer.py
├── utils/
│ ├── data.py
│ ├── filters.py
│ └── theme.py
├── data/
└── requirements.txt

Description of components:

Home.py — Landing page and prototype explanation
pages/ — Contains the main user-facing views
utils/data.py — Data loading and preprocessing
utils/filters.py — Sidebar filtering logic
utils/theme.py — UI theme and styling
data/ — Folder containing processed datasets

Requirements

To run the prototype you must have:

Python installed

All required libraries listed in requirements.txt

The necessary dataset files inside the data/ directory

The dataset must contain at minimum:

title

company

latitude

longitude

salary_min

salary_max

categoria_tag (or equivalent sector label)

Running the Application

From the root directory of the project, run the following command in your terminal:

python -m streamlit run app/Home.py

The application will open automatically in your browser at:

http://localhost:8501

Limitations (Prototype Stage)

Salary data depends on public disclosure

Geographic accuracy depends on data source quality

Machine learning models are not yet implemented

CV upload and personalized analysis are not yet available

Just to prove that is working
