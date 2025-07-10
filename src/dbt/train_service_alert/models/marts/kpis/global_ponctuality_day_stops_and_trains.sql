-- SELECT
--     DATE(feed_timestamp) AS calendar_date,
--     COUNT(*) FILTER (WHERE arrival_delay <= 300 AND departure_delay <= 300) AS nb_stops_on_time,
--     COUNT(*) AS total_stops,
--     ROUND(100.0 * COUNT(*) FILTER (WHERE arrival_delay <= 300 AND departure_delay <= 300)::NUMERIC / COUNT(*), 2) AS global_stops_punctality
-- FROM {{ ref('stg_stop_time_updates') }}
-- GROUP BY 1
-- ORDER BY 1 DESC


WITH stop_delays AS (
    SELECT
        DATE(feed_timestamp) AS calendar_date,
        COUNT(*) FILTER (WHERE arrival_delay <= 300 AND departure_delay <= 300) AS nb_stops_on_time,
        COUNT(*) AS total_stops
    FROM {{ ref('stg_stop_time_updates') }}
    GROUP BY 1
),

hourly_delays AS (
    SELECT
        trip_headsign,
        DATE(feed_timestamp) AS calendar_date,
        DATE_TRUNC('hour', feed_timestamp) AS date_hour,
        MAX(GREATEST(arrival_delay, departure_delay)) AS max_delay
    FROM {{ ref('stg_stop_time_updates') }}
    GROUP BY trip_headsign, calendar_date, date_hour
),

train_delays AS (
    SELECT
        calendar_date,
        COUNT(*) AS total_trains,
        COUNT(*) FILTER (WHERE max_delay <= 300) AS trains_on_time
    FROM hourly_delays
    GROUP BY calendar_date
)

SELECT
    sd.calendar_date,
    
    -- Stops punctuality
    sd.nb_stops_on_time,
    sd.total_stops,
    ROUND(100.0 * sd.nb_stops_on_time::NUMERIC / sd.total_stops, 2) AS global_stops_punctuality,
    
    -- Trains punctuality
    td.trains_on_time,
    td.total_trains,
    ROUND(100.0 * td.trains_on_time::NUMERIC / td.total_trains, 2) AS global_trains_punctuality

FROM stop_delays sd
LEFT JOIN train_delays td ON sd.calendar_date = td.calendar_date
ORDER BY sd.calendar_date DESC