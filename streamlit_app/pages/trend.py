import streamlit as st
import pandas as pd
import plotly.express as px
from pages.db import run_query

# # Create API client.
# credentials = service_account.Credentials.from_service_account_info(
#     st.secrets["gcp_service_account"]
# )
# client = bigquery.Client(credentials=credentials)

# @st.cache_data(ttl=600)
# def run_query(query):
#     query_job = client.query(query)
#     rows_raw = query_job.result()
#     # Convert to list of dicts. Required for st.cache_data to hash the return value.
#     rows = [dict(row) for row in rows_raw]
#     return rows

st.set_page_config(layout="wide")

st.header("Trends Page")

top_ten_tab, daily_tab, monthly_tab, countries_tab, num_kills_vs_traps_tab = st.tabs(["Top Tens Suburbs", "Daily Kills", "Monthly Kills", "Countries", "# Kills vs # Traps"])

with top_ten_tab:
    rows = run_query("""
SELECT STRIKED_YEAR, KILL_RANK, TERRITORIAL_AUTHORITY, TOWN_CITY, SUBURB_LOCALITY, TOTAL_KILLS, TOTAL_TRAPS
FROM `qut-data-analytics-capstone.goodnature.fct_nz_annual_top_ten_suburbs`;
""")
    df = pd.DataFrame(rows)

    fig = px.bar(
      df, x="KILL_RANK", y="TOTAL_KILLS", barmode="group",
      facet_col="STRIKED_YEAR",
      hover_data=["STRIKED_YEAR", "KILL_RANK", "TOTAL_KILLS", "TOTAL_TRAPS", "TERRITORIAL_AUTHORITY", "TOWN_CITY", "SUBURB_LOCALITY"],
      color="KILL_RANK",
      color_continuous_scale=px.colors.sequential.Agsunset,
      color_continuous_midpoint=5,
      text="SUBURB_LOCALITY"
    )
    st.plotly_chart(fig)


with daily_tab:
    rows = run_query("""
    WITH daily_traps_data AS (
    SELECT STRIKED_DATE,
    NUM_KILLS
    FROM `goodnature.fct_nz_daily_kills`
    )
    SELECT
        STRIKED_DATE,
        SUM(NUM_KILLS) TOTAL_KILLS
        FROM daily_traps_data
    GROUP BY STRIKED_DATE
    ORDER BY STRIKED_DATE""")


    # Perform query.
    st.header("New Zealand Trap Kill Trend")

    df = pd.DataFrame(rows)

    fig = px.line(df, x="STRIKED_DATE", y="TOTAL_KILLS")
    st.plotly_chart(fig)

with monthly_tab:
    rows = run_query("""
  WITH monthly_traps_data AS (
    SELECT
      STRIKED_YEAR_MONTH,
      STRIKED_MONTH,
      STRIKED_YEAR,
      NUM_KILLS,
      NUM_TRAPS
    FROM
      `goodnature.fct_nz_monthly_kills`
  )
    SELECT
      STRIKED_YEAR_MONTH,
      STRIKED_MONTH,
      STRIKED_YEAR,
      SUM(NUM_KILLS) TOTAL_KILLS,
      SUM(NUM_TRAPS) NUM_TRAPS
    FROM monthly_traps_data
    GROUP BY STRIKED_YEAR_MONTH, STRIKED_YEAR, STRIKED_MONTH
    ORDER BY STRIKED_YEAR, STRIKED_MONTH;
""")

    # Perform query.
    st.header("New Zealand goodnature Monthly Kills")

    df = pd.DataFrame(rows)
    df_long = df.melt(id_vars=["STRIKED_YEAR_MONTH",  "STRIKED_MONTH", "STRIKED_YEAR"],
                      value_vars=["TOTAL_KILLS", "NUM_TRAPS"],
                      var_name="Metric",
                      value_name="Value")
    color_map = {
    'TOTAL_KILLS': '#DB3069',
    'NUM_TRAPS': '#F5D547',
}
    fig = px.line(df_long, x="STRIKED_YEAR_MONTH",
                  y="Value",
                  color="Metric",
                  title="Monthly #Kills vs #Traps Over Time",
                  color_discrete_map=color_map,
                  height=800
                  )
    st.plotly_chart(fig)

with countries_tab:
  countries_stat = run_query("""
WITH countries_stat AS (
SELECT 'New Zealand' AS `Country`, COUNT(*) AS `Number of Addresses` FROM `goodnature.dim_nz_locations`
UNION ALL
SELECT 'Australia' AS `Country`, COUNT(*) AS `Number of Addresses` FROM `goodnature.dim_au_locations`
UNION ALL
SELECT 'Other countries' AS `Country`, COUNT(*) AS `Number of Addresses` FROM `goodnature.dim_intl_locations`
  ) SELECT * FROM countries_stat ORDER BY `Number of Addresses` DESC
""")
  df = pd.DataFrame(countries_stat)
  fig = px.bar(df, x="Country", y="Number of Addresses", text_auto=True, color="Country",
               color_discrete_map={'New Zealand': '#1446A0', 'Australia': '#DB3069', 'Other countries': '#F5D547'},
               title="Goodnature Trap Locations by Country")
  fig.update_layout(width=300, height=800)
  st.plotly_chart(fig)

with num_kills_vs_traps_tab:
      rows = run_query("""
  WITH monthly_traps_data AS (
    SELECT
      STRIKED_YEAR_MONTH,
      STRIKED_MONTH,
      STRIKED_YEAR,
      NUM_KILLS,
      NUM_TRAPS
    FROM
      `goodnature.fct_nz_monthly_kills`
  )
    SELECT
      STRIKED_YEAR_MONTH,
      STRIKED_MONTH,
      STRIKED_YEAR,
      SUM(NUM_KILLS) TOTAL_KILLS,
      SUM(NUM_TRAPS) NUM_TRAPS
    FROM monthly_traps_data
    GROUP BY STRIKED_YEAR_MONTH, STRIKED_YEAR, STRIKED_MONTH
    ORDER BY STRIKED_YEAR, STRIKED_MONTH;
""")
      df = pd.DataFrame(rows)
      fig = px.scatter(df, x=df["TOTAL_KILLS"], y=df["NUM_TRAPS"], hover_name=df["STRIKED_YEAR_MONTH"],
                       hover_data=["TOTAL_KILLS", "NUM_TRAPS", "STRIKED_YEAR_MONTH", "STRIKED_MONTH", "STRIKED_YEAR"],
                       color="STRIKED_YEAR")
      st.plotly_chart(fig)

