WITH aus_suburbs AS (
    SELECT
        l.location_id,
        l.latitude,
        l.longitude
    FROM {{ ref("int_trap_locations") }} l
    LEFT JOIN {{ ref("dim_nz_locations") }} d ON l.location_id = d.location_id
    WHERE d.location_id IS NULL
),

aus_suburbs_geo AS (
    SELECT
        suburb,
        urban_area,
        postcode,
        state,
        state_name,
        suburb_type,
        local_goverment_area,
        latitude,
        longitude
    FROM {{ ref('stg_au_suburbs') }}
)

SELECT
    s.location_id,
    g.suburb,
    g.urban_area,
    g.postcode,
    g.state,
    g.state_name,
    g.suburb_type,
    g.local_goverment_area,
    s.latitude AS trap_latitude,
    s.longitude AS trap_longitude,
    g.latitude AS suburb_latitude,
    g.longitude AS suburb_longitude,
    ST_DISTANCE(
    ST_GEOGPOINT(s.longitude, s.latitude),
    ST_GEOGPOINT(g.longitude, g.latitude)
    ) AS distance_in_meters
FROM
    aus_suburbs AS s
    JOIN
    aus_suburbs_geo AS g
    ON ST_DWITHIN(
        ST_GEOGPOINT(s.longitude, s.latitude),
        ST_GEOGPOINT(g.longitude, g.latitude),
        40000  -- The radius in meters. Adjust this value based on your data's density.
    )
QUALIFY ROW_NUMBER() OVER (PARTITION BY s.location_id ORDER BY distance_in_meters ASC) = 1
