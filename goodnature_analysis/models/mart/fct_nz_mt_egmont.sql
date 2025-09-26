WITH mt_egmont_area_traps AS (
SELECT
FORMAT_DATE('%Y-Q%Q', DATE(STRIKE_AT)) AS YEAR_QUARTER,
  *
FROM {{ ref("int_trap_details") }}
WHERE TRAP_LATITUDE <= -39.112449 AND TRAP_LATITUDE >= -39.386351 -- -40.313950, 170.503177
AND TRAP_LONGITUDE <= 174.173492 AND TRAP_LONGITUDE >= 173.919373 -- -43.242660, 172.741466
AND ACTIVITY_TYPE = 'STRIKE' AND STRIKE_AT >= '2017-01-01'
),

same_address_stats AS (
SELECT
YEAR_QUARTER,
  FULL_ADDRESS,
  SUBURB_LOCALITY,
  TERRITORIAL_AUTHORITY,
  COUNT(ACTIVITY_TYPE) AS NUM_KILLS,
  COUNT(DISTINCT TRAP_ID) AS NUM_TRAPS
FROM mt_egmont_area_traps
GROUP BY YEAR_QUARTER, FULL_ADDRESS, SUBURB_LOCALITY,
  TERRITORIAL_AUTHORITY
),

larger_customers AS (
SELECT * FROM same_address_stats
WHERE NUM_TRAPS >= 5
),

larger_customer_addresses AS (
SELECT
  ROW_NUMBER() OVER(PARTITION BY c.YEAR_QUARTER, c.FULL_ADDRESS) row_num,
  c.YEAR_QUARTER,
  l.full_address, l.suburb_locality, l.town_city, l.territorial_authority, l.TRAP_LATITUDE latitude,
  l.TRAP_LONGITUDE longitude, c.NUM_KILLS num_kills, c.NUM_TRAPS num_traps
FROM larger_customers c
JOIN mt_egmont_area_traps l ON l.full_address = c.full_address
)

SELECT
YEAR_QUARTER year_quarter,
full_address,
suburb_locality,
town_city, territorial_authority,
latitude,
longitude,
num_kills,
num_traps
FROM larger_customer_addresses
WHeRE row_num = 1
ORDER BY YEAR_QUARTER, SUBURB_LOCALITY, TOWN_CITY, TERRITORIAL_AUTHORITY
