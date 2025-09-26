import plotly.express as px
import pandas as pd
from pages.db import run_query
from sklearn import preprocessing
import streamlit as st
import json

st.set_page_config(layout="wide")
st.title("Traps Scatter Plot Map")
col1, col2, col3 = st.columns(3)
with col1:
    selected_year = st.selectbox(
        "Select a year",
        ["2017", "2018", "2019", "2020", "2021"],
        index=0)
with col2:
    st.text("Stats")

query = f"""
SELECT
  *
FROM `goodnature.fct_nz_daily_kills_per_trap_location`
WHERE STRIKED_YEAR = '{selected_year}'
"""

data = run_query(query)

df = pd.DataFrame(data)
min_kills = df["NUM_KILLS"].min()
max_kills = df["NUM_KILLS"].max()
min_traps = df["NUM_TRAPS"].min()
max_traps = df["NUM_TRAPS"].max()
df["NORM_KILLS"] = preprocessing.normalize(df[["NUM_KILLS"]], axis=0)*25
df["NORM_TRAPS"] = preprocessing.normalize(df[["NUM_TRAPS"]], axis=0)*25
df["KILL_RATE"] = round(df["NUM_KILLS"] / df["NUM_TRAPS"], 2)
df["TEXT"] = 'Number of kills: ' + df["NUM_KILLS"].astype(str) + ', Number of traps:' + df["NUM_TRAPS"].astype(str)

with open(f"streamlit_app/data/nz_territorial_boundary_map.json", "r") as f:
    geo_json = json.load(f)

fig = px.scatter_map(
    df,
    lon=df["TRAP_LONGITUDE"],
    lat=df["TRAP_LATITUDE"],
    hover_name=df["TEXT"],
    hover_data=["NUM_KILLS", "NUM_TRAPS", "KILL_RATE"],
    color = df['NORM_KILLS'],
    size=df['NORM_TRAPS'],
    color_continuous_scale=px.colors.sequential.Sunsetdark_r,
    size_max=25,
    center={"lat": -39.768510, "lon": 170.283173 },    zoom=5.5,
    height=1500
)
# -39.768510, 170.283173


st.plotly_chart(fig)

