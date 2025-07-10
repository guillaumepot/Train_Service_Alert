WITH recent AS (
    SELECT *
    FROM {{ ref('stg_stop_time_updates') }}
    WHERE feed_timestamp > NOW() - INTERVAL '60 minutes'
)
SELECT
    trip_headsign,
    stop_name,
    MAX(arrival_delay) AS max_arrival_delay,
    MAX(departure_delay) AS max_departure_delay
FROM recent
WHERE arrival_delay > 0
OR departure_delay > 0
GROUP BY trip_headsign, stop_name