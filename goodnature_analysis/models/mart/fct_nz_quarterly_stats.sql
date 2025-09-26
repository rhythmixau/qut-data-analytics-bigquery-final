WITH trap_data AS (
SELECT
  FORMAT_DATE('%Y-Q%Q', DATE(STRIKE_AT)) AS YEAR_QUARTER,
  TRAP_ID,
  LOCATION_ID,
  FULL_ADDRESS,
  SUBURB_LOCALITY,
  TOWN_CITY,
  TERRITORIAL_AUTHORITY,
  ACTIVITY_TYPE,
  TRAP_LATITUDE,
  TRAP_LONGITUDE,
  STRIKE_AT
FROM {{ ref('int_trap_details')}}
WHERE ACTIVITY_TYPE = 'STRIKE' AND STRIKE_AT >= '2017-01-01'
),
summary AS (
SELECT
  YEAR_QUARTER,
  FULL_ADDRESS,
  SUBURB_LOCALITY,
  TOWN_CITY,
  TERRITORIAL_AUTHORITY,
  ACTIVITY_TYPE,
  TRAP_LATITUDE,
  TRAP_LONGITUDE,
  COUNT(ACTIVITY_TYPE) NUM_KILLS,
  COUNT(DISTINCT TRAP_ID) NUM_TRAPS
FROM trap_data
GROUP BY
  YEAR_QUARTER,
  TRAP_ID,
  FULL_ADDRESS,
  SUBURB_LOCALITY,
  TOWN_CITY,
  TERRITORIAL_AUTHORITY,
  ACTIVITY_TYPE,
  TRAP_LATITUDE,
  TRAP_LONGITUDE
),
kills_traps AS (
SELECT
  YEAR_QUARTER,
  FULL_ADDRESS,
  SUBURB_LOCALITY,
  TOWN_CITY,
  TERRITORIAL_AUTHORITY,
  SUM(NUM_KILLS) NUM_KILLS,
  SUM(NUM_TRAPS) NUM_TRAPS
FROM summary
GROUP BY YEAR_QUARTER,
  FULL_ADDRESS,
  SUBURB_LOCALITY,
  TOWN_CITY,
  TERRITORIAL_AUTHORITY
), locations AS (
  SELECT
    full_address,
    address_number,
    full_road_name,
    suburb_locality,
    town_city,
    territorial_authority,
    address_latitude latitude,
    address_longitude longitude
  FROM {{ ref('dim_nz_locations')}}
),
location_kills_traps AS (
  SELECT
    ROW_NUMBER() OVER(PARTITION BY t.YEAR_QUARTER, l.full_address) AS number,
    t.YEAR_QUARTER,
    l.full_address,
    l.address_number,
    l.full_road_name,
    l.suburb_locality,
    l.town_city,
    l.territorial_authority,
    l.latitude,
    l.longitude,
    t.NUM_KILLS,
    t.NUM_TRAPS
  FROM kills_traps t
  JOIN locations l ON l.full_address = t.full_address
)
SELECT
  YEAR_QUARTER,
  full_address,
  address_number,
  full_road_name,
  suburb_locality,
  town_city,
  territorial_authority,
  latitude,
  longitude,
  NUM_KILLS,
  NUM_TRAPS
FROM location_kills_traps
WHERE number = 1
ORDER BY YEAR_QUARTER,
territorial_authority,
town_city,
suburb_locality,
num_traps,
num_kills

