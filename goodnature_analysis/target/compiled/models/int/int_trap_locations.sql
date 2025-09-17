
WITH locations AS (
    SELECT
        DISTINCT
        latitude,
        longitude
    FROM GOODNATURE.public.stg_trap_data
)
SELECT
    ROW_NUMBER() OVER(ORDER BY longitude) AS location_id,
    latitude,
    longitude
FROM locations
WHERE (longitude >= -180 AND longitude <= 180) AND (latitude >= -90 AND latitude <= 90)