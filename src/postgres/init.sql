--init.sql

-- TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;


-- Trip Updates
CREATE TABLE trip_updates (
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


CREATE TABLE stop_time_updates (
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
SELECT add_compression_policy('trip_updates',      INTERVAL '3 days');
SELECT add_compression_policy('stop_time_updates', INTERVAL '3 days');

SELECT add_retention_policy('trip_updates',      INTERVAL '90 days');
SELECT add_retention_policy('stop_time_updates', INTERVAL '90 days');



-- Service Alerts
CREATE TABLE alerts (
    feed_timestamp     TIMESTAMPTZ NOT NULL,
    alert_id           TEXT        NOT NULL,
    cause              TEXT,
    effect             TEXT,
    severity           SMALLINT,
    url                TEXT,
    header             TEXT,
    description        TEXT,
    PRIMARY KEY (alert_id, feed_timestamp)
);

SELECT create_hypertable(
    'alerts',
    'feed_timestamp',
    if_not_exists => TRUE,
    migrate_data   => TRUE
);

CREATE TABLE alert_periods (
    feed_timestamp     TIMESTAMPTZ NOT NULL,
    alert_id           TEXT        NOT NULL,
    period_seq         INT         NOT NULL,
    start_time         TIMESTAMPTZ,
    end_time           TIMESTAMPTZ,
    PRIMARY KEY (alert_id, feed_timestamp, period_seq)
);

SELECT create_hypertable(
    'alert_periods',
    'feed_timestamp',
    if_not_exists => TRUE,
    migrate_data   => TRUE
);

CREATE TABLE alert_entities (
    feed_timestamp     TIMESTAMPTZ NOT NULL,
    alert_id           TEXT        NOT NULL,
    entity_seq         INT         NOT NULL,
    agency_id          TEXT,
    route_id           TEXT,
    stop_id            TEXT,
    trip_id            TEXT,
    direction_id       SMALLINT,
    route_type         SMALLINT,
    PRIMARY KEY (alert_id, feed_timestamp, entity_seq)
);

SELECT create_hypertable(
    'alert_entities',
    'feed_timestamp',
    if_not_exists => TRUE,
    migrate_data   => TRUE
);

CREATE INDEX IF NOT EXISTS ix_alert_entities_stop  ON alert_entities (stop_id);
CREATE INDEX IF NOT EXISTS ix_alert_entities_route ON alert_entities (route_id);
CREATE INDEX IF NOT EXISTS ix_alert_entities_trip  ON alert_entities (trip_id);

ALTER TABLE alerts          SET (timescaledb.compress, timescaledb.compress_segmentby = 'alert_id');
ALTER TABLE alert_periods   SET (timescaledb.compress, timescaledb.compress_segmentby = 'alert_id');
ALTER TABLE alert_entities  SET (timescaledb.compress, timescaledb.compress_segmentby = 'alert_id');

SELECT add_compression_policy('alerts',          INTERVAL '3 days');
SELECT add_compression_policy('alert_periods',   INTERVAL '3 days');
SELECT add_compression_policy('alert_entities',  INTERVAL '3 days');

SELECT add_retention_policy('alerts',          INTERVAL '30 days');
SELECT add_retention_policy('alert_periods',   INTERVAL '30 days');
SELECT add_retention_policy('alert_entities',  INTERVAL '30 days');