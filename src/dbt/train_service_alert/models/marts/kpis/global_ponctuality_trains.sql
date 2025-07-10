WITH train_max_delays AS (
    SELECT
        trip_headsign,
        DATE(feed_timestamp) AS calendar_date,
        MAX(GREATEST(arrival_delay, departure_delay)) AS max_delay
    FROM {{ ref('stg_stop_time_updates') }}
    GROUP BY trip_headsign, calendar_date
),

train_stop_punctuality AS (
    SELECT
        trip_headsign,
        DATE(feed_timestamp) AS calendar_date,
        COUNT(*) FILTER (WHERE arrival_delay <= 300 AND departure_delay <= 300) AS nb_stops_on_time,
        COUNT(*) AS total_stops
    FROM {{ ref('stg_stop_time_updates') }}
    GROUP BY trip_headsign, calendar_date
)

SELECT
    p.trip_headsign,
    p.calendar_date,

    -- Stop-level punctuality
    p.nb_stops_on_time,
    p.total_stops,
    ROUND(100.0 * p.nb_stops_on_time::NUMERIC / p.total_stops, 2) AS ponctuality_train_per_stop_pct,

    -- Max delay punctuality
    d.max_delay,
    CASE WHEN d.max_delay <= 300 THEN TRUE ELSE FALSE END AS is_on_time

FROM train_stop_punctuality p
LEFT JOIN train_max_delays d
  ON p.trip_headsign = d.trip_headsign AND p.calendar_date = d.calendar_date
ORDER BY p.calendar_date DESC, p.trip_headsign
