-- created_at: 2025-09-16T22:41:35.591654+00:00
-- dialect: bigquery
-- node_id: not available
-- desc: execute adapter call

    select distinct schema_name from `qut-data-analytics-capstone`.INFORMATION_SCHEMA.SCHEMATA;
  ;
-- created_at: 2025-09-16T22:41:38.604039+00:00
-- dialect: bigquery
-- node_id: model.goodnature_analysis.fct_nz_daily_kills
-- desc: get_relation adapter call
SELECT table_catalog,
                    table_schema,
                    table_name,
                    table_type
                FROM `qut-data-analytics-capstone`.`goodnature`.INFORMATION_SCHEMA.TABLES
                WHERE table_name = 'fct_nz_daily_kills';
-- created_at: 2025-09-16T22:41:40.457978+00:00
-- dialect: bigquery
-- node_id: model.goodnature_analysis.fct_nz_daily_kills
-- desc: execute adapter call


  create or replace view `qut-data-analytics-capstone`.`goodnature`.`fct_nz_daily_kills`
  OPTIONS()
  as WITH trap_records AS (
    SELECT * FROM `qut-data-analytics-capstone`.`goodnature`.`int_trap_details`
    WHERE ACTIVITY_TYPE = 'STRIKE'
)

SELECT
    LOCATION_ID,
    TRAP_ID,
    ADDRESS_LATITUDE,
    ADDRESS_LONGITUDE,
    FULL_ADDRESS,
    FULL_ROAD_NAME,
    SUBURB_LOCALITY,
    TOWN_CITY,
    TERRITORIAL_AUTHORITY,
    ACTIVITY_TYPE,
    FORMAT_DATE('%Y-%m-%d', CAST(STRIKE_AT AS TIMESTAMP)) STRIKED_DATE,
    COUNT(STRIKE_AT) AS NUM_KILLS,
    CREATED_BY
FROM trap_records
GROUP BY LOCATION_ID,
    TRAP_ID,
    ADDRESS_LATITUDE,
    ADDRESS_LONGITUDE,
    FULL_ADDRESS,
    FULL_ROAD_NAME,
    SUBURB_LOCALITY,
    TOWN_CITY,
    TERRITORIAL_AUTHORITY,
    ACTIVITY_TYPE,
    STRIKED_DATE,
    CREATED_BY;

;
