import plotly.express as px
import pandas as pd
from pages.db import run_query
import streamlit as st
import json

st.set_page_config(layout="wide")
st.title("Traps Scatter Plot Map")
col1, col2 = st.columns(2)
with col1:
    quarters_query = """
    SELECT
        DISTINCT YEAR_QUARTER
    FROM `goodnature.fct_nz_quarterly_stats`
    ORDER BY YEAR_QUARTER;
    """
    quarters = run_query(quarters_query)
    quarters_df = pd.DataFrame(quarters)
    selected_year = st.selectbox(
        "Select a QUARTER",
        quarters_df["YEAR_QUARTER"],
        index=0)
with col2:
    st.text("Stats")

query = f"""
SELECT
*
FROM `goodnature.fct_nz_quarterly_stats`
WHERE YEAR_QUARTER = '{selected_year}' AND NUM_TRAPS > 5
ORDER BY
NUM_TRAPS DESC,
NUM_KILLS DESC;
"""

data = run_query(query)
if len(data) > 0:
    df = pd.DataFrame(data)
    df["TEXT"] = 'Address: ' + df["full_address"] + ' Territory: ' + df["territorial_authority"]


    with open(f"streamlit_app/data/nz_territorial_boundary_map.json", "r") as f:
        geo_json = json.load(f)

    fig = px.scatter_map(
        df,
        lon=df["longitude"],
        lat=df["latitude"],
        hover_name=df["TEXT"],
        hover_data=["NUM_TRAPS", "NUM_KILLS"],
        color = df['NUM_TRAPS'],
        size=df['NUM_KILLS'],
        color_continuous_scale=px.colors.sequential.Sunsetdark_r,
        size_max=25,
        center={"lat": -39.768510, "lon": 170.283173 }, zoom=5.5,
        height=1500
    )
    # -39.768510, 170.283173
    st.plotly_chart(fig)
else:
    st.text("No data available")

