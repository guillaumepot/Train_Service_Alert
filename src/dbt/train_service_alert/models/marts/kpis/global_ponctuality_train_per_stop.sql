SELECT
    trip_headsign,
    DATE(feed_timestamp) AS calendar_date,
    DATE_TRUNC('hour', feed_timestamp) AS date_hour,
    COUNT(*) FILTER (WHERE arrival_delay <= 300 AND departure_delay <= 300) AS nb_stops_on_time,
    COUNT(*) AS total_stops,
    ROUND(100.0 * COUNT(*) FILTER (WHERE arrival_delay <= 300 AND departure_delay <= 300)::NUMERIC / COUNT(*), 2) AS ponctuality_pct
FROM {{ ref('stg_stop_time_updates') }}
GROUP BY trip_headsign, calendar_date, date_hour
ORDER BY calendar_date DESC, date_hour DESC, trip_headsign