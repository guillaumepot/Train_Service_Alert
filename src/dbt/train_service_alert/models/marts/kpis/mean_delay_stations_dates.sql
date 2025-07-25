SELECT
    stop_name,
    DATE(feed_timestamp) AS calendar_date,
    ROUND(AVG(arrival_delay), 2) AS avg_arrival_delay,
    ROUND(AVG(departure_delay), 2) AS avg_departure_delay,
    COUNT(*) AS nb_trains
FROM {{ ref('stg_stop_time_updates') }}
GROUP BY stop_name, calendar_date
ORDER BY calendar_date DESC, stop_name