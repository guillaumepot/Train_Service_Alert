SELECT
    DATE(feed_timestamp) AS calendar_date,
    COUNT(*) FILTER (WHERE arrival_delay <= 300 AND departure_delay <= 300) AS nb_stops_on_time,
    COUNT(*) AS total_stops,
    ROUND(100.0 * COUNT(*) FILTER (WHERE arrival_delay <= 300 AND departure_delay <= 300)::NUMERIC / COUNT(*), 2) AS ponctuality_percentage
FROM {{ ref('stg_stop_time_updates') }}
GROUP BY 1
ORDER BY 1 DESC