WITH non_nz_locations AS (
SELECT
    l.location_id,
    l.latitude,
    l.longitude
  FROM {{ ref("int_trap_locations") }} l
  LEFT JOIN {{ ref("dim_nz_locations") }} d ON l.location_id = d.location_id
  WHERE d.location_id IS NULL
),

aus_locations AS (
  SELECT
    location_id,
    trap_latitude,
    trap_longitude
  FROM
    {{ ref("dim_au_locations") }}
)

SELECT
  n.*
FROM non_nz_locations n
LEFT JOIN aus_locations a ON a.location_id = n.location_id
WHERE a.location_id IS NULL
