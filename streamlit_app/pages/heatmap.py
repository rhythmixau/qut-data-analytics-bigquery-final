import json
import streamlit as st
from pages.db import run_query
import plotly.express as px
import pandas as pd

island_districts = {
    "North Island": [
        "Auckland",
        "Carterton District",
        "Central Hawke's Bay District",
        "Far North District",
        "Gisborne District",
        "Hamilton City",
        "Hastings District",
        "Hauraki District",
        "Horowhenua District",
        "Hutt City",
        "Kaipara District",
        "Kapiti Coast District",
        "Kawerau District",
        "Manawatu District",
        "Masterton District",
        "Matamata-Piako District",
        "Napier City",
        "New Plymouth District",
        "Ōpōtiki District",
        "Ōtorohanga District",
        "Palmerston North City",
        "Porirua City",
        "Rangitikei District",
        "Rotorua Lakes District",
        "Ruapehu District",
        "South Taranaki District",
        "South Waikato District",
        "South Wairarapa District",
        "Stratford District",
        "Tararua District",
        "Taupo District",
        "Tauranga City",
        "Thames-Coromandel District",
        "Upper Hutt City",
        "Waipa District",
        "Waikato District",
        "Wairoa District",
        "Waitomo District",
        "Wellington City",
        "Western Bay of Plenty District",
        "Whakatane District",
        "Whanganui District",
        "Whangarei District"],
    "South Island": [
        "Ashburton District",
        "Buller District",
        "Central Otago District",
        "Chatham Islands Territory",
        "Christchurch City",
        "Clutha District",
        "Dunedin City",
        "Gore District",
        "Grey District",
        "Hurunui District",
        "Invercargill City",
        "Kaikōura District",
        "Mackenzie District",
        "Marlborough District",
        "Nelson City",
        "Queenstown-Lakes District",
        "Selwyn District",
        "Southland District",
        "Tasman District",
        "Timaru District",
        "Waimakariri District",
        "Waimate District",
        "Waitaki District",
        "Westland District"
    ]
}

if "island" not in st.session_state:
    st.session_state.island = list(island_districts.keys())[0]

col1, col2, col3 = st.columns(3)
with col1:
    selected_year = st.selectbox(
        "Select a year",
        ["2017", "2018", "2019", "2020", "2021"],
        index=0)
with col2:
    selected_island = st.radio(
        "Select an island",
        key="island",
        options=island_districts.keys(),
        index=0
    )

with col3:
    territory_name = st.selectbox(
        "Select a district",
        island_districts[selected_island],
        index=0)

query = f"""
WITH trap_data AS (
  SELECT
    FORMAT_DATE('%Y', CAST(STRIKED_DATE AS DATE)) AS YEAR,
    TERRITORIAL_AUTHORITY,
    TOWN_CITY,
    SUBURB_LOCALITY,
    NUM_KILLS,
    NUM_TRAPS
  FROM `goodnature.fct_nz_daily_kills`
  WHERE TERRITORIAL_AUTHORITY = "{territory_name}"
),
  trap_summary AS (
  SELECT
    YEAR,
    TERRITORIAL_AUTHORITY,
    TOWN_CITY,
    SUBURB_LOCALITY,
    SUM(NUM_KILLS) NUM_KILLS,
    SUM(NUM_TRAPS) NUM_TRAPS
  FROM trap_data
  WHERE YEAR = '{selected_year}'
  GROUP BY YEAR, TERRITORIAL_AUTHORITY, TOWN_CITY, SUBURB_LOCALITY
  ), --1593 ROWS
  suburbs_in_district AS (
    SELECT DISTINCT TERRITORIAL_AUTHORITY,
    TOWN_CITY,
    SUBURB_LOCALITY
    FROM `goodnature.stg_nz_addresses`
    WHERE TERRITORIAL_AUTHORITY = "{territory_name}"
  ),
  trap_data_with_default AS (
    SELECT
      IFNULL(s.YEAR, '{selected_year}') YEAR,
      d.TERRITORIAL_AUTHORITY,
      d.TOWN_CITY,
      d.SUBURB_LOCALITY,
      IFNULL(s.NUM_KILLS, 0) NUM_KILLS,
      IFNULL(s.NUM_TRAPS, 0) NUM_TRAPS
    FROM suburbs_in_district d
    LEFT JOIN trap_summary s ON d.SUBURB_LOCALITY = s.SUBURB_LOCALITY
  ),
  map_data AS (
    SELECT id, name, name_ascii
    FROM `goodnature.nz_suburb_locality`
  ),
  summary_with_row_nums AS (
  SELECT
    ROW_NUMBER() OVER(PARTITION BY s.TERRITORIAL_AUTHORITY, s.TOWN_CITY, s.SUBURB_LOCALITY ORDER BY m.id) AS ROW_NUM,
    m.id as LOCATION_ID,
    s.TERRITORIAL_AUTHORITY,
    s.TOWN_CITY,
    s.SUBURB_LOCALITY,
    m.name,
    m.name_ascii,
    s.NUM_KILLS,
    s.NUM_TRAPS
  FROM trap_data_with_default s
  JOIN map_data m ON s.SUBURB_LOCALITY = m.name_ascii OR s.SUBURB_LOCALITY = m.name
  )
  SELECT
    LOCATION_ID,
    TERRITORIAL_AUTHORITY,
    TOWN_CITY,
    SUBURB_LOCALITY,
    name SUBURB_NAME,
    name_ascii SUBURB_NAME_ASCII,
    NUM_KILLS,
    NUM_TRAPS
  FROM summary_with_row_nums
  WHERE ROW_NUM = 1
  ORDER BY TERRITORIAL_AUTHORITY, TOWN_CITY, SUBURB_LOCALITY
"""
kill_stats = run_query(query)

kill_stats_df = pd.DataFrame(kill_stats)
with open(f"streamlit_app/data/nz_{territory_name}_map.json", "r") as f:
    geo_json = json.load(f)

with open(f"streamlit_app/data/territory_centres_2.json", "r") as f:
    territory_centres = json.load(f)

center = territory_centres[territory_name]

st.set_page_config(layout="wide")

if len(kill_stats) > 0:
    max_kill = kill_stats_df["NUM_KILLS"].max()
    min_kill = kill_stats_df["NUM_KILLS"].min()

    fig = px.choropleth_map(kill_stats_df, geojson=geo_json, locations="LOCATION_ID",
                            # featureidkey="properties.id"
                            color="NUM_KILLS",
                            color_continuous_scale=px.colors.sequential.Agsunset,
                            range_color=(0, max_kill),
                            map_style="carto-positron",
                            zoom=8, center={"lat": center["lat"], "lon": center["lon"]},
                            opacity=0.5,
                            labels={"NUM_KILLS": "Number of Kills"},
                            height=800
                            )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)
else:
    st.text("No data available")

