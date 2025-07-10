SELECT
    a.alert_id,
    stu.trip_headsign,
    a.active_period_start,
    a.active_period_end,
    a.cause,
    a.effect,
    a.severity,
    a.header_fr,
    a.description_fr
FROM {{ source('gtfs', 'alerts') }} a
JOIN {{ source('gtfs', 'alert_entities') }} ae ON a.alert_id = ae.alert_id
JOIN {{ ref('stg_stop_time_updates') }} stu ON ae.trip_id = stu.trip_id
WHERE active_period_start <= NOW()
  AND (active_period_end IS NULL OR active_period_end > NOW())