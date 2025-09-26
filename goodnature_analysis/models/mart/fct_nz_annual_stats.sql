WITH  trap_data AS (
SELECT
  FORMAT_DATE('%Y', CAST(STRIKED_DATE AS DATE)) AS YEAR,
  *
FROM {{ ref('fct_nz_daily_kills') }}
WHERE STRIKED_DATE >= '2017-01-01' AND ACTIVITY_TYPE = 'STRIKE'
),
territorial_authorites AS (
  SELECT TA2025_V1_00 territory_id,
    TA2025_V1_00_NAME territory_name,
    TA2025_V1_00_NAME_ASCII territory_name_ascii
  FROM {{ source('gcp_cloud', 'territorial_authorities') }} WHERE TA2025_V1_00 IS NOT NULL
),
years AS (
  SELECT DISTINCT YEAR FROM trap_data WHERE YEAR IS NOT NULL
),
yearly_territorial_authorities AS (
  SELECT y.YEAR, ta.*
  FROM years y,
  territorial_authorites ta
  ORDER BY y.YEAR, ta.territory_name
),
territorial_summary AS (
  SELECT
    YEAR,
    TERRITORIAL_AUTHORITY,
    COUNT(DISTINCT SUBURB_LOCALITY) NUM_SUBURBS,
    COUNT(DISTINCT TOWN_CITY) NUM_TOWNS,
    SUM(NUM_KILLS) NUM_KILLS,
    SUM(NUM_TRAPS) NUM_TRAPS
  FROM trap_data
  GROUP BY YEAR, TERRITORIAL_AUTHORITY
),
territories_stats AS (
  SELECT
    TERRITORIAL_AUTHORITY,
    COUNT(DISTINCT suburb_locality) NUM_SUBURBS,
    COUNT(DISTINCT town_city) NUM_TOWNS
  FROM {{ ref('stg_nz_addresses') }}
  WHERE territorial_authority IS NOT NULL
  GROUP BY TERRITORIAL_AUTHORITY
),
yearly_territories_stats AS (
  SELECT YEAR, s.*
  FROM years,
  territories_stats s
),
territorial_final_stats AS (
SELECT
  t.YEAR,
  a.territory_id TERRITORY_AUTHORITY_ID,
  t.TERRITORIAL_AUTHORITY,
  IFNULL(s.NUM_SUBURBS, 0) NUM_SUBURBS,
  t.NUM_SUBURBS TOTAL_NUM_SUBURBS,
  IFNULL(s.NUM_TOWNS, 0) NUM_TOWNS,
  t.NUM_TOWNS TOTAL_NUM_TOWNS,
  IFNULL(s.NUM_KILLS, 0) NUM_KILLS,
  IFNULL(s.NUM_TRAPS, 0) NUM_TRAPS
FROM yearly_territories_stats t
JOIN yearly_territorial_authorities a ON (t.TERRITORIAL_AUTHORITY = a.territory_name OR t.TERRITORIAL_AUTHORITY = a.territory_name_ascii) AND t.YEAR = a.YEAR
LEFT JOIN territorial_summary s ON t.TERRITORIAL_AUTHORITY = s.TERRITORIAL_AUTHORITY AND t.YEAR = s.YEAR
)
SELECT
  YEAR,
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
ORDER BY YEAR, TERRITORIAL_AUTHORITY
