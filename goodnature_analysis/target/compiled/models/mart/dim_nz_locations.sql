

WITH locations AS (
    SELECT
        location_id,
        latitude,
        longitude
    FROM `qut-data-analytics-capstone`.`goodnature`.`int_trap_locations`
), addresses AS (
    SELECT
        address_id,
        full_address,
        full_address_number,
        full_road_name,
        suburb_locality,
        town_city,
        territorial_authority,
        water_name,
        water_body_name,
        longitude,
        latitude
    FROM `qut-data-analytics-capstone`.`goodnature`.`stg_nz_addresses`
)
SELECT
    loc.location_id,
    addr.full_address,
    addr.full_address_number AS address_number,
    addr.full_road_name,
    addr.suburb_locality,
    addr.town_city,
    addr.territorial_authority,
    loc.longitude AS trap_longitude,
    loc.latitude AS trap_latitude,
    addr.longitude AS address_longitude,
    addr.latitude AS address_latitude,
    ST_DISTANCE(
        ST_GEOGPOINT(loc.longitude, loc.latitude),
        ST_GEOGPOINT(addr.longitude, addr.latitude)
    ) AS distance_in_meters
FROM
    locations AS loc
    JOIN
    addresses AS addr
    ON ST_DWITHIN(
        ST_GEOGPOINT(loc.longitude, loc.latitude),
        ST_GEOGPOINT(addr.longitude, addr.latitude),
        20000  -- The radius in meters. Adjust this value based on your data's density.
)
QUALIFY ROW_NUMBER() OVER (PARTITION BY loc.location_id ORDER BY distance_in_meters ASC) = 1