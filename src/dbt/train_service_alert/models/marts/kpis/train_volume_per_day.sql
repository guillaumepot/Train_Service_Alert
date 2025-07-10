SELECT
    start_date AS calendar_date,
    COUNT(DISTINCT trip_id) AS nb_trains
FROM {{ source('gtfs', 'trip_updates') }}
GROUP BY calendar_date
ORDER BY calendar_date DESC