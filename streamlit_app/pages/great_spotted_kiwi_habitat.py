import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pages.db import run_query
import streamlit as st
import json

st.set_page_config(layout="wide")
st.title("Great Spotted Kiwi Habitats")

sum_query = f"""
SELECT
year_quarter,
SUM(num_kills) num_kills,
SUM(num_traps) num_traps
FROM `goodnature.fct_nz_great_spotted_kiwi`
GROUP BY year_quarter
"""

quarterly_summary = run_query(sum_query)
quarterly_df = pd.DataFrame(quarterly_summary)

summary_fig = go.Figure(data=[
    go.Bar(name="Number of Kills", x=quarterly_df["year_quarter"], y=quarterly_df["num_kills"], marker_color="#C10900"),
    go.Bar(name="Number of Traps", x=quarterly_df["year_quarter"], y=quarterly_df["num_traps"], marker_color="#FFD700")
])
summary_fig.update_layout(barmode="group", title_text="Trap Activities in the Great Spotted Kiwi Habitats",
                          xaxis_title_text="Year and Quarter",
                          yaxis_title_text="Number of Kills/Traps",
                          legend=dict(
                              orientation="h",
                              yanchor="bottom",
                              y=-0.3,
                              xanchor="center",
                              x=0.1
                          ))
st.plotly_chart(summary_fig)


col1, col2 = st.columns(2)
with col1:
    quarters_query = """
    SELECT
        DISTINCT year_quarter
    FROM `goodnature.fct_nz_great_spotted_kiwi`
    ORDER BY year_quarter;
    """
    quarters = run_query(quarters_query)
    quarters_df = pd.DataFrame(quarters)
    selected_year = st.selectbox(
        "Select a QUARTER",
        quarters_df["year_quarter"],
        index=0)
with col2:
    st.text("Stats")

query = f"""
SELECT
*
FROM `goodnature.fct_nz_great_spotted_kiwi`
WHERE year_quarter = '{selected_year}'
ORDER BY year_quarter, num_kills DESC, num_traps DESC
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
        hover_data=["num_traps", "num_kills"],
        color = df['num_traps'],
        size=df['num_kills'],
        color_continuous_scale=px.colors.sequential.Sunsetdark_r,
        size_max=25,
        center={"lat": -41.779707, "lon": 172.635257 }, zoom=7, # ,
        height=1000
    )
    # -39.768510, 170.283173
    st.plotly_chart(fig)

else:
    st.text("No data available")

