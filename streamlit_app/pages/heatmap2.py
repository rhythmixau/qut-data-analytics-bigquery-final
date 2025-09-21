import json
import streamlit as st
from pages.db import run_query
import plotly.express as px
import pandas as pd

col1, col2, col3 = st.columns(3)
with col1:
    selected_year = st.selectbox(
        "Select a year",
        ["2017", "2018", "2019", "2020", "2021"],
        index=0)
with col2:
    selected_measure = st.selectbox(
        "Select a measure",
        ["NUM_KILLS", "NUM_TRAPS", "SUBURB_COVERAGE_PERCENTAGE", "TOWN_COVERAGE_PERCENTAGE", "NUM_SUBURBS", "NUMB_TOWNS"],
        index=0)

with col3:
    st.text("Stats")

measures_labels = {
  "NUM_KILLS": "Number of Kills",
  "NUM_TRAPS": "Number of Traps",
  "SUBURB_COVERAGE_PERCENTAGE": "Suburb Coverage Percentage",
  "TOWN_COVERAGE_PERCENTAGE": "Town Coverage Percentage",
  "NUM_SUBURBS": "Number of Suburbs",
  "NUMB_TOWNS": "Number of Towns"
}

query = f"""
WITH  trap_data AS (
SELECT
  *
FROM `goodnature.fct_nz_daily_kills`
WHERE STRIKED_DATE >= '2017-01-01' AND ACTIVITY_TYPE = 'STRIKE' AND FORMAT_DATE('%Y', CAST(STRIKED_DATE AS DATE)) = '{selected_year}'
),
territorial_authorites AS (
  SELECT TA2025_V1_00 territory_id,
    TA2025_V1_00_NAME territory_name,
    TA2025_V1_00_NAME_ASCII territory_name_ascii
  FROM `goodnature.territorial_authorities` WHERE TA2025_V1_00 IS NOT NULL
),
territorial_summary AS (
  SELECT
    TERRITORIAL_AUTHORITY,
    COUNT(DISTINCT SUBURB_LOCALITY) NUM_SUBURBS,
    COUNT(DISTINCT TOWN_CITY) NUM_TOWNS,
    SUM(NUM_KILLS) NUM_KILLS,
    SUM(NUM_TRAPS) NUM_TRAPS
  FROM trap_data
  GROUP BY TERRITORIAL_AUTHORITY
),
territories_stats AS (
  SELECT
    TERRITORIAL_AUTHORITY,
    COUNT(DISTINCT suburb_locality) NUM_SUBURBS,
    COUNT(DISTINCT town_city) NUM_TOWNS
  FROM `goodnature.stg_nz_addresses`
  WHERE territorial_authority IS NOT NULL
  GROUP BY TERRITORIAL_AUTHORITY
),
territorial_final_stats AS (
SELECT
  a.territory_id TERRITORY_AUTHORITY_ID,
  t.TERRITORIAL_AUTHORITY,
  IFNULL(s.NUM_SUBURBS, 0) NUM_SUBURBS,
  t.NUM_SUBURBS TOTAL_NUM_SUBURBS,
  IFNULL(s.NUM_TOWNS, 0) NUM_TOWNS,
  t.NUM_TOWNS TOTAL_NUM_TOWNS,
  IFNULL(s.NUM_KILLS, 0) NUM_KILLS,
  IFNULL(s.NUM_TRAPS, 0) NUM_TRAPS
FROM territories_stats t
JOIN territorial_authorites a ON t.TERRITORIAL_AUTHORITY = a.territory_name OR t.TERRITORIAL_AUTHORITY = a.territory_name_ascii
LEFT JOIN territorial_summary s ON t.TERRITORIAL_AUTHORITY = s.TERRITORIAL_AUTHORITY
)
SELECT
  TERRITORY_AUTHORITY_ID,
  TERRITORIAL_AUTHORITY,
  NUM_SUBURBS,
  TOTAL_NUM_SUBURBS,
  (NUM_SUBURBS/TOTAL_NUM_SUBURBS)*100.0 AS SUBURB_COVERAGE_PERCENTAGE,
  NUM_TOWNS,
  TOTAL_NUM_TOWNS,
  (NUM_TOWNS/TOTAL_NUM_TOWNS)*100.0 AS TOWN_COVERAGE_PERCENTAGE,
  NUM_KILLS,
  NUM_TRAPS
FROM territorial_final_stats
ORDER BY TERRITORIAL_AUTHORITY
"""
territorial_stats = run_query(query)

territorial_stats_df = pd.DataFrame(territorial_stats)
with open(f"streamlit_app/data/nz_territorial_boundary_map.json", "r") as f:
    geo_json = json.load(f)

st.set_page_config(layout="wide")



if len(territorial_stats) > 0:
    match selected_measure:
        case "NUM_KILLS":
          max_value = territorial_stats_df["NUM_KILLS"].max()
        case "NUM_TRAPS":
          max_value = territorial_stats_df["NUM_TRAPS"].max()
        case "SUBURB_COVERAGE_PERCENTAGE":
          max_value = territorial_stats_df["SUBURB_COVERAGE_PERCENTAGE"].max()
        case "TOWN_COVERAGE_PERCENTAGE":
          max_value = territorial_stats_df["TOWN_COVERAGE_PERCENTAGE"].max()
        case "NUM_SUBURBS":
          max_value = territorial_stats_df["NUM_SUBURBS"].max()
        case "NUMB_TOWNS":
          max_value = territorial_stats_df["NUM_TOWNS"].max()

    fig = px.choropleth_map(territorial_stats_df, geojson=geo_json, locations="TERRITORY_AUTHORITY_ID",
                            # featureidkey="properties.id"
                            color=selected_measure,
                            color_continuous_scale=px.colors.sequential.Agsunset,
                            range_color=(0, max_value),
                            map_style="carto-positron",
                            zoom=5, center={"lat": -41.649690, "lon": 173.959537},
                            opacity=0.5,
                            labels={selected_measure: measures_labels[selected_measure]},
                            hover_data=["TERRITORIAL_AUTHORITY", "NUM_SUBURBS", "NUM_TOWNS", "NUM_KILLS", "NUM_TRAPS", "SUBURB_COVERAGE_PERCENTAGE", "TOWN_COVERAGE_PERCENTAGE"],
                            height=800
                            )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)
else:
    st.text("No data available")

