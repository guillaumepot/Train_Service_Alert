SELECT
    trip_headsign,
    ROUND(AVG(arrival_delay), 2) AS avg_arrival_delay,
    RANK() OVER (ORDER BY AVG(arrival_delay) DESC) AS rank
FROM {{ ref('stg_stop_time_updates') }}
GROUP BY trip_headsign