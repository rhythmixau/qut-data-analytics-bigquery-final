import streamlit as st

st.set_page_config(layout="wide")
st.title("Project Journal")
st.markdown("### Module 1")
st.markdown("##### 27 July 2025 - Jack Toke []")
st.markdown("""
Goodnature, a New Zealand-based company, manufactures traps that humanely kill mice and rats. Unlike traditional
poisons or methods that cause prolonged suffering, these traps are designed for an instant kill.

My analysis will focus on trap data, beginning with the initial setup time and including a record of every time a trap
strikes a rat or mouse. The primary purpose of this initiative extends beyond simple pest control; it's a conservation
effort aimed at preventing the extinction of native bird species and helping their populations recover.

My initial thoughts on this data is that there are many empty columns and some columns such as 'batteryLevel'
are not going to tell us much as the values are either blank or 100.  What is the most confusing are the 'when' and
'trapInstalledAt' columns.  The values of the 'when' and 'trapInstalledAt' columns, for the most part, are equal,
except that they are microseconds apart and both are months if not years after the strikeTime.  I am speculating
that this is due the difference in system clocks on the server computer and the trap themselves.  As far as I am
concerned the 'when' and 'trapInstalledAt' columns are not going to offer me anything meaningful, in relation to
conservation work.

I am therefore going to focus on making sense of the data using the 'activityType', 'strikeAt', 'latitude' and
'longitude' columns. Although 'batchId', 'createdBy' and 'trapId' columns may offer us something useful due to
the time constraint I won't be able to study them.

By next week, I will have to decide the tech stack I am going to use in helping me analyse and manage the data.  Then
I will have to start setting up the project and start to analyse the data.

Todo list:
1. Setup the Airflow, Snowflake and dbt project.
2. Start cleaning the data and load them into the database.
3. Start the data exploration.
            """)
st.image("streamlit_app/images/raw_data.jpg", caption="Raw goodnature trap data")

st.markdown("### Module 2")
st.markdown("##### 3 August 2025")
st.markdown("""
I have decided that I am going to use 'dbt', 'Snowflake' and 'Streamlit' for data visualisation and for keeping records
of my project journal.  Since we are not going to regularly update the data, I am dropping off the Airflow from the
stack.

**Initial observation:**
There are 9 trap activity types and they are 'STRIKE', 'TEST_STRIKE', 'SYNCED', 'CO2_LOW', 'LURE_LOW', 'NO_CO2_LEFT',
'UNCOLLECTED_DATA', CO2_REPLACED AND 'LURE_REPLACED'.
Depending on what we are trying to analyse, different activity types may be of interest to us.  I am interested
in the performance of the traps in terms of the number of rats killed and the native New Zealand birds conservation
effort.  Thus I'll be interested in studying the number of rats killed in different regions, towns and cities in New
Zealand.

It is awesome that the latitude and longitude data are available, but we will need a way to reverse them into addresses
so we can figure out the town, cities or suburbs the traps were located, so our analysis maybe more meaningful.

Python library, 'geopy', could potentially be useful in obtaining the addresses of these GPS coordinates.  However,
each request does take approximately 1 second, and this is going to be time consuming.  Making individual requests for each
row is not going to make sense as there are a million rows.  We can try to filter out unique GPS coordinates to reduce
the number of requests.

I performed a quick query, filtering out unique GPS coordinates, for 'STRIKE' activity type only and we still have
**83,434** rows.  Thus using 'geopy' library is out of the question, as it is not very convenient and extremely time consuming.

Snowflake does have ST_DWITHIN, ST_DISTANCE and a few other methods that we may be able to calculate the nearest
known address to a given GPS coordinate.  We will first need to find New Zealand's publicly available addresses, which
hopefully will not be as time consuming.

Fortunately, [Land Information New Zealand](https://data.linz.govt.nz/layer/105689-nz-addresses/) website publishes
all the addresses in New Zealand.  This could be useful as I could just load it into the data and find the nearest
address to each GPS coordinate.

At this point, I can analyse the number of kills in each location on daily, monthly and annual basis.  It would help
if I could visualise the data on some kind of heatmap, such as Chloropleth map by Plotly Express.  This we will need
to obtain the suburb boundary data for the whole country.

To-do list:
1. Find a useable New Zealand suburb or locality boundary data, so we can plot the map and maybe that might help us
find some new insights.
2. Figure out how to plot the heatmap using Plotly Express.
""")

st.markdown("### Module 3")
st.markdown("##### 10 August 2025")
st.markdown("""
**Challenges:** There are a number of challenges with the available data.  The boundary data come in the WKT format,
but Plotly Express requires the data to in a different shape.  This mean I will have further transform the geometry
data using square brackets and commas instead of the WKT format.
""")
st.code("""
# WKT format
WKT,id,parent_id,name,type,start_date,name_ascii
"MULTIPOLYGON (((175.822161002875 -39.1292319975892,175.822496996572 -39.1291279965885, ...)))
        """)

st.code("""
# Square brackets and commas
{'type': 'Feature',
 'properties': {'GEO_ID': '0500000US01001',
  'STATE': '01',
  'COUNTY': '001',
  'NAME': 'Autauga',
  'LSAD': 'County',
  'CENSUSAREA': 594.436},
 'geometry': {'type': 'Polygon',
  'coordinates': [[[-86.496774, 32.344437],
    [-86.717897, 32.402814],
    [-86.814912, 32.340803],
    [-86.890581, 32.502974],
    [-86.917595, 32.664169],
    [-86.71339, 32.661732],
    [-86.714219, 32.705694],
    [-86.413116, 32.707386],
    [-86.411172, 32.409937],
    [-86.496774, 32.344437]]]},
 'id': '01001'}
""")
st.markdown("""
I am having issues loading geodata into the database, as the suburb boundaries geometry data is stored as strings, they
can be very long, exceeding the maximum length limit.  I can't seem to increase the maximum length, no matter what I do.

Todo:
1. Explore other analytics database options - DuckDB or BigQuery
""")

st.markdown("### Module 4")
st.markdown("##### 17 August 2025")
st.markdown("""
I have switched the database to DuckDB/MotherDuck.  There's been performance issue with MotherDuck cloud database.
Even loading the initial 1 million rows into the database is taking too long.  After waiting for almost 45 minutes
the trap data is loaded.  I tried loading the Geodata and the waited for over an hour without much success.  Maybe
it's a CPU resource issue.  However, even after upgrading to a paid tier at USD$25 a month, there was no improvement.

I am now going to have to switch to BigQuery and see if I can get better performance without having field length
limits.
1. Switch to BigQuery
""")

st.markdown("### Module 5")
st.markdown("##### 31 August2025")
st.markdown("""
BigQuery has better performance, but there is an Organisation Policy that restricts data access to the public, which
is necessary if I were to make the data available on the Streamlit website.  I have tried to create custom rules to
allow public access to the data with no success.  After fighting with Gemini over how to modify the organisation
policy to allow public access I have given up on the idea and resolve to disabling the policy.
""")

st.code("""
constraint: constraints/iam.allowedPolicyMemberDomains
listPolicy:
  allValues: ALLOW
""")

st.markdown("""
I have better luck with BigQuery.  The geodata file loaded quickly.  I needed the data to be loaded into the database,
in order to ensure that the names of the suburb, towns or cities, and territories from the address dataset and the
suburb boundaries are lining up so I can properly crease the heatmap using Plotly Express chloropleth graph.

I tried using dbt Python model to transform the geodata but it requires extra permissions to other Google Cloud resources.
I think this is making things too complicated, and I have resolved to using pure Python to transform the WKT geometry
 data into the square bracket format as shown in module 3.
""")

st.markdown("""
Instead of loading the data via dbt, directly create the table and load the data into BigQuery.
""")
st.code("""
CREATE OR REPLACE EXTERNAL TABLE `qut-data-analytics-capstone.goodnature.nz_suburb_locality`
(
  WKT STRING,
  id INT64,
  parent_id INT64,
  name STRING,
  type STRING,
  start_date STRING,
  name_ascii STRING
)
OPTIONS(
  format = 'CSV',
  skip_leading_rows = 1,
  uris = ['gs://qut-capstone-data/raw/nz_suburb_locality.csv']
);
""")

st.markdown("""
I have successfully transformed the geodata into the shape that is required by Plotly Express.  However the file is over
1GB in size.  That is problematic because Streamlit cannot load the whole file as it has a size limit of 250MB.
The question now is, how do I break up the files into sizeable chunks?  I think breaking it up by the districts or
territories makes sense.  This way, I can add a dropdown on the Streamlit page which will allow us to select the
district I want to see.

#### Convert MULTIPOLYGON to brackets and at the same time break them up into smaller files.""")

st.code("""
import pandas as pd
import json

def space_to_bracket(pair: str):
    values = pair.split(" ")
    return [float(values[0]), float(values[1])]

def wkt_to_coordinates(wkt_value: str):
    wkt_value = wkt_value.replace("MULTIPOLYGON ", "").replace(")", "").replace("(", "")
    val_pairs = wkt_value.split(",")
    coordinates = [space_to_bracket(pair) for pair in val_pairs]
    return [coordinates]

def model():
    map_df = pd.read_csv("goodnature_analysis/seeds/nz_suburb_locality.csv")
    nz_addresses_df = pd.read_csv("goodnature_analysis/seeds/nz_addresses.csv")

    territorial_authorities = nz_addresses_df["territorial_authority"].dropna().unique()
    territorial_suburbs = {territory: nz_addresses_df[nz_addresses_df["territorial_authority"] == territory]["suburb_locality"].dropna().unique().tolist() for territory in territorial_authorities}

    with open('streamlit_app/data/territorial_suburbs.json', 'w') as f:
        json.dump(territorial_suburbs, f, indent=4)

    map_df["coordinates"] = map_df["WKT"].apply(wkt_to_coordinates)
    map_df = map_df[["id", "parent_id","name","type","start_date","name_ascii", "coordinates"]]
    map_df["parent_id"] = map_df["parent_id"].fillna(0).astype(int)

    for territory in territorial_authorities:
        territory_map_df = map_df[map_df["name"].isin(territorial_suburbs[territory])]

        # map_df.to_json("streamlit/data/nz_suburbs_map.json", orient="records")
        locations = [{'type': 'Feature',
            'properties': {
            'id': row["id"],
            'parent_id': row['parent_id'],
            'name': row['name'],
            'type': row['type'],
            'start_date': row['start_date'],
            'name_ascii': row['name_ascii']},
            'geometry': {'type': 'Polygon',
            'coordinates': row["coordinates"]},
            'id': f'{row["id"]}'
        } for _, row in territory_map_df.iterrows()]
        map_dict = {'type': 'FeatureCollection', 'features': locations}
        with open(f'streamlit_app/data/nz_{territory}_map.json', 'w') as f:
            json.dump(map_dict, f, indent=4)

def main():
    print("Loading file")
    model()
""")

st.markdown("""
The file is now divided into 67 smaller files, which are more acceptable for Streamlit, one for each territory/district authority.

To-do list:
1. Start visualising the data in Streamlit
""")

st.markdown("### Module 6")
st.markdown("##### 7 September 2025")
st.markdown("""I want to see the number of kills and number of traps in each suburb.""")

st.code("""
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
""")

st.markdown("""
We can now visualise the data, but since data is not available for every suburb, there are empty spaces in the map.
A solution to that may be to apply default values where there are no trap data and set the number of kills to 0.  Doing
this will allow us to see the suburbs where there is no data alongside the suburbs with values.
""")

st.image("streamlit_app/images/suburb_level_chloropleth2.jpg", caption="Suburb level chloropleth - Kaipara District")

st.markdown("""
After adding the default values, i.e. 0, to suburbs where there is no data, I can see that much of the suburbs in a
large proportion of the territories do not have data, even if that is changing over the years.  It is probably better
to zoom out and view the statistics at territory level.
""")

st.markdown("### Module 7")
st.markdown("##### 14 September 2025")
st.markdown("Convert the boundary line data fromMULTIPOLYGON to bracket pairs")
st.code("""
import pandas as pd
import json

def space_to_bracket(pair: str):
    values = pair.split(" ")
    return [float(values[0]), float(values[1])]

def wkt_to_coordinates(wkt_value: str):
    wkt_value = wkt_value.replace("MULTIPOLYGON ", "").replace(")", "").replace("(", "")
    val_pairs = wkt_value.split(",")
    coordinates = [space_to_bracket(pair) for pair in val_pairs]
    return [coordinates]

def model():

    nz_territories_df = pd.read_csv("goodnature_analysis/seeds/territorial_authority_2025.csv")

    nz_territories_df["coordinates"] = nz_territories_df["WKT"].apply(wkt_to_coordinates)
    nz_territories_df = nz_territories_df[["TA2025_V1_00", "TA2025_V1_00_NAME", "TA2025_V1_00_NAME_ASCII", "LAND_AREA_SQ_KM", "AREA_SQ_KM", "SHAPE_Length", "coordinates"]]


    # map_df.to_json("streamlit/data/nz_suburbs_map.json", orient="records")
    territorial_authorities_boundaries = [{'type': 'Feature',
        'properties': {
        'territorial_id': row["TA2025_V1_00"],
        'territorial_name': row['TA2025_V1_00_NAME'],
        'territorial_name_ascii': row['TA2025_V1_00_NAME_ASCII'],
        'land_area_sq_km': row['LAND_AREA_SQ_KM'],
        'area_sq_km': row['LAND_AREA_SQ_KM'],
        'shape_length': row['SHAPE_Length']},
        'geometry': {'type': 'Polygon',
        'coordinates': row["coordinates"]},
        'id': f'{row["TA2025_V1_00"]}'
    } for _, row in nz_territories_df.iterrows()]
    map_dict = {'type': 'FeatureCollection', 'features': territorial_authorities_boundaries}
    with open(f'streamlit_app/data/nz_territorial_boundary_map.json', 'w') as f:
        json.dump(map_dict, f, indent=4)

def main():
    print("Loading file")
    model()
""")
st.markdown("Load the territory geo data into the database")
st.code("""
CREATE OR REPLACE EXTERNAL TABLE `qut-data-analytics-capstone.goodnature.territorial_authorities`
(
    WKT STRING,
    TA2025_V1_00 INT64,
    TA2025_V1_00_NAME STRING,
    TA2025_V1_00_NAME_ASCII STRING,
    LAND_AREA_SQ_KM FLOAT64,
    AREA_SQ_KM FLOAT64,
    SHAPE_Length FLOAT64
)
OPTIONS(
    format = 'CSV',
    skip_leading_rows = 1,
    uris = ['gs://qut-capstone-data/raw/territorial_authority_2025.csv']
);
""")
st.markdown("""
With the district or territory level data fully loaded into the database, we can start to formulate a query to get the
basic summary of kills, number of traps, number of towns and suburbs our traps are being deployed.
""")
st.code("""
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
""")
st.image("streamlit_app/images/territory_level_chloropleth.jpg", caption="Territory level chloropleth")
st.text("https://savethekiwi.nz/about-kiwi/where-to-see-kiwi/")
st.markdown("""
Now that we can see the big picture of the statistics,  we can start analysing the data.
""")
st.image("streamlit_app/images/kiwi_habitats.png", caption="https://savethekiwi.nz/about-kiwi/where-to-see-kiwi/")
st.markdown("### Module 8")
st.markdown("##### 21 September 2025")
st.image("streamlit_app/images/kea_habitat_map.jpg", caption="Kea Birds Habitat Map")
st.text("https://www.arcgis.com/apps/mapviewer/index.html?panel=gallery&suggestField=true&layers=79ea1d1b63fa436ca8702b1d459b4e7f")
st.markdown("""
**Questions:**
1. Do the habitats of Kea and Kiwi overlap?

It seems like some Kiwis and Keas do share habitats.  However, Keas only live on the South Island, while Kiwi area also
found further north of the North Island.

2. Is there goodnature trap activities in those areas?

On the South Island goodnature traps are more concentrated in the Fiordland National Park.

3. How is the growth in those areas over the years?

There's definitely growth in the whole country but some areas have seen more growth than others.

4. Which area may need more attention?

Mount Aspiring National Park and Ōkārito may need some more attention.

""")

st.markdown("""
I have created a new plot using Scatter Plot Map.  I think this will give us the most accurate understanding of the
situation, as it doesn't take away the detail of what's happening on the ground.  I have simply sum up the number of
kills and traps per GPS coordinate.  We can partition the visualisation by the year and we can see the change after
each year.
""")

st.code("""
SELECT
  FORMAT_DATE('%Y', CAST(STRIKE_AT AS TIMESTAMP)) as STRIKED_YEAR,
  TRAP_LONGITUDE,
  TRAP_LATITUDE,
  COUNT(DISTINCT STRIKE_AT) AS NUM_KILLS,
  COUNT(DISTINCT TRAP_ID) AS NUM_TRAPS
FROM {{ ref('int_trap_details') }}
WHERE ACTIVITY_TYPE = 'STRIKE' AND STRIKE_AT IS NOT NULL
GROUP BY STRIKED_YEAR, TRAP_LONGITUDE, TRAP_LATITUDE
ORDER BY NUM_KILLS DESC, NUM_TRAPS DESC
""")
st.markdown("#### The result:")
st.image("streamlit_app/images/scatter_plot_map.jpg", caption="Scatter Plot Map")

st.markdown("""
To achieve this, I have normalised the number of kills and the number of traps.  So when some locations have a really
high number of kills or number of traps, then the rest of locations with just a few kills become very hard to see.
Normalising the values give us a good range to plot without losing or distorting the meaning of the data.
""")
st.code("""
query = f'
SELECT
  *
FROM `goodnature.fct_nz_daily_kills_per_trap_location`
WHERE STRIKED_YEAR = '{selected_year}'
'

data = run_query(query)

df = pd.DataFrame(data)
min_kills = df["NUM_KILLS"].min()
max_kills = df["NUM_KILLS"].max()
min_traps = df["NUM_TRAPS"].min()
max_traps = df["NUM_TRAPS"].max()
df["NORM_KILLS"] = preprocessing.normalize(df[["NUM_KILLS"]], axis=0)*25
df["NORM_TRAPS"] = preprocessing.normalize(df[["NUM_KILLS"]], axis=0)*25
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
    color = df['NORM_TRAPS'],
    size=df['NORM_KILLS'],
    color_continuous_scale=px.colors.sequential.Sunsetdark_r,
    size_max=25,
    zoom=4,
    height=800
)

st.plotly_chart(fig)
""")
st.markdown("""

To-do list:
1. Analyse the trap data and see which area may need more focus.
2. Complete the project report
""")

# rates, proportions and percentage
# Circular or periodic data
# dates and times
