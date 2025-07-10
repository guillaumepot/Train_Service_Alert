WITH hourly_delays AS (
    SELECT
        trip_headsign,
        DATE(feed_timestamp) AS calendar_date,
        DATE_TRUNC('hour', feed_timestamp) AS date_hour,
        MAX(GREATEST(arrival_delay, departure_delay)) AS max_delay
    FROM {{ ref('stg_stop_time_updates') }}
    GROUP BY trip_headsign, calendar_date, date_hour
)
SELECT
    calendar_date,
    date_hour,
    COUNT(*) AS total_trains,
    COUNT(*) FILTER (WHERE max_delay <= 300) AS trains_ponctuels,
    ROUND(100.0 * COUNT(*) FILTER (WHERE max_delay <= 300)::NUMERIC / COUNT(*), 2) AS ponctuality_pct
FROM hourly_delays
GROUP BY calendar_date, date_hour
ORDER BY calendar_date DESC, date_hour DESC