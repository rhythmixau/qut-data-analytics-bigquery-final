WITH traps AS (
    SELECT
        *
    FROM `qut-data-analytics-capstone`.`goodnature`.`goodnature_trap_data`
)
SELECT
    id,
    uploadTime AS uploaded_at,
    activityType AS activity_type,
    strikeTime AS strike_at,
    batchId AS batch_id,
    createdBy AS created_by,
    trapId AS trap_id,
    latitude,
    longitude,
    batteryLevel AS battery_level,
    hasImage AS has_image,
    trapInstalledAt AS installed_at
FROM traps