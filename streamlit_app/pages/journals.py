import streamlit as st

st.title("Project Journal")
st.markdown("### Module 1")
st.markdown("##### 27 July 2025")
st.markdown("""
Goodnature, a New Zealand-based company, manufactures traps that humanely kill mice and rats. Unlike traditional
poisons or methods that cause prolonged suffering, these traps are designed for an instant kill.

Our analysis will focus on trap data, beginning with the initial setup time and including a record of every time a trap
strikes a rat or mouse. The primary purpose of this initiative extends beyond simple pest control; it's a conservation
effort aimed at preventing the extinction of native bird species and helping their populations recover.

My initial thoughts on this data is that there are many empty columns and some columns such as 'batteryLevel'
are not going to tell us much as the values are either blank or 100.  What is confusing the most are 'when' and
'trapInstalledAt' columns.  The values of the 'when' and 'trapInstalledAt' columns, for the most part, are equal,
except that they are microseconds apart and both are months if not years after the strikeTime.  I am speculating
that this is due the difference in system clocks on the server computer and the trap themselves.  As far as I am
concerned the 'when' and 'trapInstalledAt' columns are not going to offer us anything meaningful.

I am therefore going to focus on making sense of the data using the 'activityType', 'strikeAt', 'latitude' and
'longitude' columns. Although 'batchId', 'createdBy' and 'trapId' columns may offer us something useful, but due to
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
Depending on what we are trying to analyse, different activity types maybe of interest to us.  I am interested
in the performance of the traps in term of the number of rats killed and the native New Zealand birds conservation
effort.  Thus I'll be interested in studying the number of rats killed in different regions, towns and cities in New
Zealand.

It is awesome that the latitude and longitude data are available, but we will need a way to reverse them into addresses
so we can figure out the town, cities or suburbs the traps were located, so our analysis maybe more meaningful.

Python library, 'geopy', could potentially be useful in obtaining the addresses of these GPS coordinates.  However,
each request does take approximately 1 second, and this is going to be time consuming.  Making individual request for each
row is not going to make sense as there are a million rows.  We can try to filter out unique GPS coordinates to reduce
the number of requests.

I performed a quick query, filtering out unique GPS coordinates, for 'STRIKE' activity type only and we still have
**83,434** rows.  Thus using 'geopy' library is out of question, as it is not going to be very convenient and time consuming.

Snowflake does have ST_DWITHIN, ST_DISTANCE and a few other methods that we maybe able to calculate the nearest
known address to a given GPS coordinate.  We will first need to find New Zealand publicly available addresses, which
hopeful will not be as time consuming.

Fortunately, [Land Information New Zealand](https://data.linz.govt.nz/layer/105689-nz-addresses/) website publishes
all the addresses in New Zealand.  This could be useful as I could just load it into the data and find the nearest
address to each GPS coordinate.

At this point, I can analyse the number of kills in each location on daily, monthly and annual basis.  It would help
if I could visualise the data on some kinds of heatmap, such as Chloropleth map by Plotly Express.  This we will need
to obtain the suburb boundary data for the whole country.

Todo list:
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
I am having issue loading geodata into the database, as the suburb boundaries geometry data are stored as strings, they
can be very long exceeding the maximum length limit.  I can't seem to increase the maximum length, no matter what I do.

Todo:
1. Explore other analytics database options - DuckDB or BigQuery
""")
st.markdown("### Module 4")
st.markdown("##### 17 August 2025")
st.markdown("""
I have switch the database to DuckDB/MotherDuck.  There's been performance issue with MotherDuck cloud database.
Even loading the initial 1 million rows into the database is taking very long.  After waiting for almost 45 minutes
the trap data is loaded.  I tried loading the Geodata and the waited for over an hour without much success.  Maybe
it's a CPU resource issue.  However, even after upgrading to a paid tier at USD$25 a month, there was no improvement.

I am now going to have to switch to BigQuery and see if I could get better performance without having field length
limits.
1. Switch to BigQuery
""")

st.markdown("### Module 5")
st.markdown("##### 31 August2025")
st.markdown("""
BigQuery has better performance, but there is an Organisation Policy that restrict data access to the public, which
is necessary if I were to make the data available on the Streamlit website.  I have tried to create custom rule to
allow public access to the data, but without success.  After fighting with Gemini over how to modify the organisation
policy to allow public access I have given up on the idea and resolve to disabling the policy.

I have better luck with BigQuery.  The geodata file loaded quickly.  I needed the data to be loaded into the database,
in order to ensure that the names of the suburb, towns or cities, and territories from the address dataset and the
suburb boundaries are lining up so I can properly crease the heatmap using Plotly Express chloropleth graph.

I tried using dbt Python model to transform the geodata but it requires extra permission to other Google Cloud resources.
I think this is making things too complicated, and I have resolved to using pure Python to transform the WKT geometry
 data into the square bracket format as shown in module 3.

I have successfully transform the geodata into the shape that is required by Plotly Express.  However the file is over
1GB in size.  That is problematic because Streamlit cannot load the whole file as it has a size limit of just 250MB.
The question now is, how do I break up the files into sizeable chunks?  I think breaking it up by the districts or
territories makes sense.  This way, I can add a dropdown on the Streamlit page which will allow us to select the
district we want to see.

The file is now divided into 67 smaller files, which are more acceptable for Streamlit, one for each territory or
territory authority.

1. Start visualising the data in Streamlit
""")

st.markdown("### Module 6")
st.markdown("##### 7 September 2025")
st.markdown("""
We can now visualise the data, but since data are not available for every suburb, there are empty spaces in the map.
A solution to that maybe to apply default values where there are no trap data and set the number of kills to 0.  Doing
this will allow us to see the suburbs where there is no data beside those with some values.

After adding the default 0 to suburbs where there is no data, I can see that much of the suburbs in a large proportion
of the territories do not have data, even if that is changing over the years.  It is probably better to zoom out and
""")

st.markdown("### Module 7")
st.markdown("##### 14 September 2025")

st.markdown("### Module 8")
st.markdown("##### 21 September 2025")

# rates, proportions and percentage
# Circular or periodic data
# dates and times
