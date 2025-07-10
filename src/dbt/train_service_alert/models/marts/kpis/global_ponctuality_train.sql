WITH daily_max_delays AS (
    SELECT
        trip_headsign,
        DATE(feed_timestamp) AS calendar_date,
        MAX(GREATEST(arrival_delay, departure_delay)) AS max_delay
    FROM {{ ref('stg_stop_time_updates') }}
    GROUP BY trip_headsign, calendar_date
)

SELECT
    trip_headsign,
    calendar_date,
    max_delay,
    CASE WHEN max_delay <= 300 THEN TRUE ELSE FALSE END AS is_on_time
FROM daily_max_delays
ORDER BY calendar_date DESC, trip_headsign