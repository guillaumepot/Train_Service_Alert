WITH base AS (
    SELECT
        stu.feed_timestamp,
        stu.trip_id,
        SUBSTRING(stu.trip_id FROM 'OCESN([0-9]+)') AS trip_headsign,
		s.stop_name,
		s.stop_lat,
		s.stop_lon,
		s.location_type,
        stu.stop_index,
		stu.arrival_time,
        {{ normalize_delay('arrival_delay') }} AS arrival_delay,
		stu.departure_time,
        {{ normalize_delay('departure_delay') }} AS departure_delay
    FROM {{ source('gtfs', 'stop_time_updates') }} stu
    LEFT JOIN {{ source('gtfs', 'stops') }} s ON stu.stop_id = s.stop_id
)
SELECT * FROM base