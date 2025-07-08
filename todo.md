-> DBT
-> BI
-> (API)
-> CI/CD pipeline


SELECT t.trip_id, t.trip_headsign, t.direction_id, r.route_long_name,
	   st.arrival_time, st.departure_time, st.stop_sequence, st.pickup_type, st.drop_off_type,
	   s.stop_name, s.stop_lat, s.stop_lon, s.location_type
FROM trips t
JOIN routes r ON r.route_id = t.route_id
JOIN stop_times st ON t.trip_id = st.trip_id
JOIN stops s on s.stop_id = st.stop_id
WHERE r.route_type = 2
-- AND t.trip_id LIKE 'OCESN89%'

SELECT *
FROM trip_updates;


SELECT *
FROM trips;


**services**
docker compose --profile database up -d
docker compose --profile administration up -d
docker compose --profile pipeline up -d

**GTFS update:**
docker compose --profile gtfs-update up


**Config**
Secrets:
postgres_user.secret
postgres_password.secret



