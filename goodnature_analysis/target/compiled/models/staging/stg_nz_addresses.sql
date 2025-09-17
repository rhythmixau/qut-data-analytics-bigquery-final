WITH addresses AS (
    SELECT
        *
    FROM GOODNATURE.public.nz_addresses
)
SELECT
    WKT,
    address_id,
    source_dataset,
    change_id,
    full_address_number,
    full_road_name,
    full_address,
    territorial_authority,
    unit_type,
    unit_value,
    level_type,
    level_value,
    address_number_prefix,
    address_number,
    address_number_suffix,
    address_number_high,
    road_name_prefix,
    road_name,
    road_type_name,
    road_suffix,
    water_name,
    water_body_name,
    suburb_locality,
    town_city,
    address_class,
    address_lifecycle,
    gd2000_xcoord,
    gd2000_ycoord,
    road_name_ascii,
    water_name_ascii,
    water_body_name_ascii,
    suburb_locality_ascii,
    town_city_ascii,
    full_road_name_ascii,
    full_address_ascii,
    shape_X AS longitude,
    shape_Y AS latitude
FROM addresses
WHERE (shape_X >= -180 AND shape_X <= 180) AND (shape_Y >= -90 AND shape_Y <= 90)