WITH suburbs AS (
    SELECT * FROM GOODNATURE.public.australian_suburbs
)
SELECT
    ssc_code AS suburb_id,
    suburb,
    urban_area,
    postcode,
    state,
    state_name,
    type AS suburb_type,
    local_goverment_area,
    statistic_area,
    elevation,
    population,
    median_income,
    sqkm,
    lat AS latitude,
    lng AS longitude,
    timezone AS suburb_timezone
FROM suburbs