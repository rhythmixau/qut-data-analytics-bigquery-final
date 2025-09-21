import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

st.set_page_config(layout="wide")

st.header("Trends Page")

top_ten_tab, daily_tab, monthly_tab = st.tabs(["Top Tens Suburbs", "Daily Kills", "Monthly Kills"])

with top_ten_tab:
    rows = run_query("""
SELECT STRIKED_YEAR, KILL_RANK, TERRITORIAL_AUTHORITY, TOWN_CITY, SUBURB_LOCALITY, TOTAL_KILLS, TOTAL_TRAPS
FROM `qut-data-analytics-capstone.goodnature.fct_nz_annual_top_ten_suburbs`;
""")
    df = pd.DataFrame(rows)

    fig = px.bar(df, x="KILL_RANK", y="TOTAL_KILLS", barmode="group",
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
      NUM_KILLS
    FROM
      `goodnature.fct_nz_monthly_kills`
  )
    SELECT
      STRIKED_YEAR_MONTH,
      STRIKED_MONTH,
      STRIKED_YEAR,
      SUM(NUM_KILLS) TOTAL_KILLS
    FROM monthly_traps_data
    GROUP BY STRIKED_YEAR_MONTH, STRIKED_YEAR, STRIKED_MONTH
    ORDER BY STRIKED_YEAR, STRIKED_MONTH;
""")

    # Perform query.
    st.header("New Zealand goodnature Monthly Kills")

    df = pd.DataFrame(rows)

    fig = px.line(df, x="STRIKED_YEAR_MONTH", y="TOTAL_KILLS")
    st.plotly_chart(fig)
