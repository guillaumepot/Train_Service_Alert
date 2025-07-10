SELECT
    trip_headsign,
    DATE(feed_timestamp) AS calendar_date,
    ROUND(AVG(arrival_delay), 2) AS avg_arrival_delay,
    ROUND(AVG(departure_delay), 2) AS avg_departure_delay,
    COUNT(*) AS nb_stops
FROM {{ ref('stg_stop_time_updates') }}
GROUP BY trip_headsign, calendar_date
ORDER BY calendar_date DESC, trip_headsign