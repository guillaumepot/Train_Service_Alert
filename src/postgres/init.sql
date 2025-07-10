--init.sql

-- TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;


-- Trip Updates
CREATE TABLE IF NOT EXISTS trip_updates (
    feed_timestamp     TIMESTAMPTZ NOT NULL,
    trip_id            TEXT        NOT NULL,
    start_time         TIME        NOT NULL,
    start_date         DATE        NOT NULL,
    PRIMARY KEY (trip_id, feed_timestamp)
);

SELECT create_hypertable(
    'trip_updates',
    'feed_timestamp',
    if_not_exists => TRUE,
    migrate_data   => TRUE
);

CREATE INDEX IF NOT EXISTS ix_trip_updates_trip ON trip_updates (trip_id);


CREATE TABLE IF NOT EXISTS stop_time_updates (
    feed_timestamp     TIMESTAMPTZ NOT NULL,
    trip_id            TEXT        NOT NULL,
    stop_index         SMALLINT    NOT NULL,
    stop_id            TEXT        NOT NULL,
    arrival_time       TIMESTAMPTZ,
    departure_time     TIMESTAMPTZ,
    arrival_delay      INT,
    departure_delay    INT,
    PRIMARY KEY (trip_id, feed_timestamp, stop_index)
);

SELECT create_hypertable(
    'stop_time_updates',
    'feed_timestamp',
    if_not_exists => TRUE,
    migrate_data   => TRUE
);

CREATE INDEX IF NOT EXISTS ix_stu_stop  ON stop_time_updates (stop_id);
CREATE INDEX IF NOT EXISTS ix_stu_trip  ON stop_time_updates (trip_id, stop_id);

ALTER TABLE trip_updates      SET (timescaledb.compress, timescaledb.compress_segmentby = 'trip_id');
ALTER TABLE stop_time_updates SET (timescaledb.compress, timescaledb.compress_segmentby = 'trip_id');
SELECT add_compression_policy('trip_updates',      INTERVAL '30 days');
SELECT add_compression_policy('stop_time_updates', INTERVAL '30 days');

SELECT add_retention_policy('trip_updates',      INTERVAL '1095 days');
SELECT add_retention_policy('stop_time_updates', INTERVAL '1095 days');



-- Service Alerts
CREATE TABLE IF NOT EXISTS alerts (
    alert_id           TEXT        NOT NULL,
    active_period_start         TIMESTAMPTZ,
    active_period_end           TIMESTAMPTZ,
    cause                       TEXT,
    effect                      TEXT,
    severity                    TEXT,
    header_en                   TEXT,
    description_en              TEXT,
    header_fr                   TEXT,
    description_fr              TEXT,
    PRIMARY KEY (alert_id, active_period_start, active_period_end)
);

SELECT create_hypertable(
    'alerts',
    'active_period_start',
    'active_period_end',
    if_not_exists => TRUE,
    migrate_data   => TRUE
);


CREATE INDEX IF NOT EXISTS ix_alerts_alert_id  ON alerts (alert_id);

ALTER TABLE alerts      SET (timescaledb.compress, timescaledb.compress_segmentby = 'alert_id');
SELECT add_compression_policy('alerts',      INTERVAL '30 days');
SELECT add_retention_policy('alerts',      INTERVAL '1095 days');


CREATE TABLE IF NOT EXISTS alert_entities (
    trip_id            TEXT        NOT NULL,
    alert_id           TEXT        NOT NULL,
    PRIMARY KEY (alert_id, trip_id)
);


-- GTFS Data
CREATE TABLE IF NOT EXISTS agency (
    agency_id          TEXT        NOT NULL,
    agency_name        TEXT        NOT NULL,
    agency_url         TEXT        NOT NULL,
    agency_timezone    TEXT        NOT NULL,
    agency_lang        TEXT        NOT NULL,
    PRIMARY KEY (agency_id)
);

CREATE TABLE IF NOT EXISTS stop_times (
    trip_id            TEXT        NOT NULL,
    arrival_time       TIME,
    departure_time     TIME,
    stop_id            TEXT        NOT NULL,
    stop_sequence      INT         NOT NULL,
    pickup_type        SMALLINT,
    drop_off_type      SMALLINT,
    PRIMARY KEY (trip_id, stop_sequence)
);

CREATE TABLE IF NOT EXISTS routes (
    route_id           TEXT        NOT NULL,
    agency_id          TEXT        NOT NULL,
    route_short_name   TEXT        NOT NULL,
    route_long_name    TEXT        NOT NULL,
    route_type         SMALLINT    NOT NULL,
    PRIMARY KEY (route_id)
);

CREATE TABLE IF NOT EXISTS trips (
    route_id           TEXT        NOT NULL,
    service_id         TEXT        NOT NULL,
    trip_id            TEXT        NOT NULL,
    trip_headsign      TEXT,
    direction_id       SMALLINT,
    block_id           TEXT,
    PRIMARY KEY (trip_id)
);


CREATE TABLE IF NOT EXISTS stops (
    stop_id            TEXT        NOT NULL,
    stop_name          TEXT        NOT NULL,
    stop_lat           FLOAT       NOT NULL,
    stop_lon           FLOAT       NOT NULL,
    location_type      SMALLINT,
    parent_station     TEXT,
    PRIMARY KEY (stop_id)
);

-- Add foreign keys
ALTER TABLE stop_times ADD FOREIGN KEY (trip_id) REFERENCES trips(trip_id);
ALTER TABLE stop_times ADD FOREIGN KEY (stop_id) REFERENCES stops(stop_id);
ALTER TABLE routes ADD FOREIGN KEY (agency_id) REFERENCES agency(agency_id);
ALTER TABLE trips ADD FOREIGN KEY (route_id) REFERENCES routes(route_id);