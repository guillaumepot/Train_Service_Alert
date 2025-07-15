# src/consumer/consumer.py
"""
Extract GTFS RT messages from Kafka, process them and save them to the database
"""
from datetime import datetime, timezone
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, ConfigResource, ConfigResourceType
import json
import os
import time
from typing import List, Tuple

from PostgreEngine import PostgreEngine

DATA_SOURCES_FILEPATH = os.getenv('DATA_SOURCES_FILEPATH', 'config/data_sources.json')


def read_secret_or_env(secret_name, env_name = None):
    """
    Read a secret from Docker secrets file, fallback to environment variable
    
    Args:
        secret_name: Name of the secret file in /run/secrets/
        env_name: Environment variable name (defaults to secret_name.upper())
    
    Returns:
        The secret value or None if not found
    """
    if env_name is None:
        env_name = secret_name.upper()
    
    secret_path = f'/run/secrets/{secret_name}'
    try:
        with open(secret_path, 'r') as f:
            value = f.read().strip()
            if value:
                return value
    except (FileNotFoundError, IOError, PermissionError):
        pass
    
    return os.getenv(env_name)


class GTFSConsumer:
    def __init__(self, var_dict:dict):
        self.var_dict = var_dict
        self.trip_update_consumer = self.get_consumer('gtfs-rt-tu', 'gtfs-rt-consumer')
        self.service_alert_consumer = self.get_consumer('gtfs-rt-sa', 'gtfs-rt-consumer')



    # Time formatting functions
    def unix_to_datetime(self, unix_timestamp):
        """Convert Unix timestamp to datetime object with UTC timezone"""
        if unix_timestamp is None:
            return None
        try:
            return datetime.fromtimestamp(int(unix_timestamp), tz=timezone.utc)
        except (ValueError, OSError):
            return None

    def format_time(self, time_str):
        """Format time string to HH:MM:SS format if needed"""
        if time_str is None:
            return None
        # If it's already in correct format, return as is
        if isinstance(time_str, str) and ':' in time_str:
            return time_str
        # If it's a Unix timestamp, convert to time format
        try:
            dt = datetime.fromtimestamp(int(time_str), tz=timezone.utc)
            return dt.strftime('%H:%M:%S')
        except (ValueError, OSError):
            return time_str

    def format_date(self, date_str):
        """Format date string to YYYY-MM-DD format if needed"""
        if date_str is None:
            return None
        # If it's already in correct format, return as is
        if isinstance(date_str, str) and '-' in date_str:
            return date_str
        # If it's in YYYYMMDD format, convert to YYYY-MM-DD
        if isinstance(date_str, str) and len(date_str) == 8:
            return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        return date_str

    # Consumer message functions
    def get_consumer(self, topic:str, group_id:str) -> KafkaConsumer:
        """Get a Kafka consumer for a given topic and group ID"""
        consumer = KafkaConsumer(topic,
                                 bootstrap_servers = self.var_dict['KAFKA_BROKERS'],
                                 auto_offset_reset = 'earliest',
                                 enable_auto_commit = True,
                                 group_id = group_id,
                                 value_deserializer = lambda m: json.loads(m.decode('utf-8'))
                                    )
        return consumer

    def consume_messages(self, consumer: KafkaConsumer, timeout_ms:int = 1000, max_messages:int = 1000) -> List[dict]:
        """Consume messages from a Kafka consumer"""
        consumed_data = []
        messages = consumer.poll(timeout_ms = timeout_ms, max_records = max_messages)
        for topic_partition, records in messages.items():
            for message in records:
                message_data = message.value
                consumed_data.append(message_data)
        return consumed_data

    def close_consumer(self, consumer: KafkaConsumer) -> None:
        """Close a Kafka consumer"""
        consumer.close()

    def set_topic_config(self, topic:str, config:dict = None) -> None:
        """Set the configuration for a Kafka topic"""
        if not config:
            config = {
                "retention.ms": "3600000",  # 1 hour retention
                "cleanup.policy": "delete",  # Delete old messages
                "segment.ms": "60000",     # 1 minute segment roll
                "delete.retention.ms": "60000"  # Delete tombstones after 1 minute
            }

        resource = ConfigResource(ConfigResourceType.TOPIC, topic)
        resource.configs = {key: str(value) for key, value in config.items()}

        admin_client = KafkaAdminClient(bootstrap_servers = self.var_dict['KAFKA_BROKERS'])
        admin_client.alter_configs([resource])
        admin_client.close()

    # Data transformation functions
    def decompose_tu_data(self, tu_data:List[dict]) -> Tuple[List[dict], List[dict]]:
        """Decompose trip update data into trip updates and stop time updates"""
        trip_updates = []
        stop_time_updates = []

        for elt in tu_data:
            try:
                trip_id = elt['id']
                start_time = self.format_time(elt['trip_update']['trip'].get('startTime'))
                start_date = self.format_date(elt['trip_update']['trip'].get('startDate'))
                feed_timestamp = self.unix_to_datetime(elt['trip_update'].get('timestamp'))

                # Trip updates data
                trip_updates.append({
                    'feed_timestamp': feed_timestamp,
                    'trip_id': trip_id,
                    'start_time': start_time,
                    'start_date': start_date
                })

                stop_index = 0 # Departure station
                for stop_time_update in elt['trip_update'].get('stopTimeUpdate', []):
                    stop_id = stop_time_update.get('stopId')
                    
                    if not stop_id:
                        continue
       
                    if 'departure' in stop_time_update:
                        departure_time = self.unix_to_datetime(stop_time_update['departure'].get('time'))
                        departure_delay = stop_time_update['departure'].get('delay')
                    else:
                        departure_time = None
                        departure_delay = None
                    
                    if 'arrival' in stop_time_update:
                        arrival_time = self.unix_to_datetime(stop_time_update['arrival'].get('time'))
                        arrival_delay = stop_time_update['arrival'].get('delay')
                    else:
                        arrival_time = departure_time
                        arrival_delay = 0

                    if not departure_time:
                        departure_time = arrival_time
                    if not departure_delay:
                        departure_delay = arrival_delay

                    # Stop time updates data
                    stop_time_updates.append({
                        'feed_timestamp': feed_timestamp,
                        'trip_id': trip_id,
                        'stop_index': stop_index,
                        'stop_id' : stop_id,
                        'arrival_time' : arrival_time,
                        'departure_time' : departure_time,
                        'arrival_delay' : arrival_delay,
                        'departure_delay' : departure_delay
                    })

                    stop_index += 1
                    
            except (KeyError, TypeError) as e:
                print(f"Error processing trip update {elt.get('id', 'unknown')}: {e}")
                continue

        return trip_updates, stop_time_updates

    def decompose_sa_data(self, sa_data:List[dict]) -> Tuple[List[dict], List[dict]]:
        """Decompose service alert data into alerts and alert entities"""
        alerts = []
        entities = []

        for elt in sa_data:
            try:
                alert_id = elt['id']
                
                active_periods = elt.get('alert', {}).get('activePeriod', [])
                if active_periods:
                    active_period_start = self.unix_to_datetime(active_periods[0].get('start'))
                    active_period_end = self.unix_to_datetime(active_periods[0].get('end'))
                else:
                    active_period_start = None # Keep None instead of 'unknown' cause datetime format
                    active_period_end = None # Keep None instead of 'unknown' cause datetime format


                for entity in elt.get('alert', {}).get('informedEntity', []):
                    trip_info = entity.get('trip', {})
                    trip_id = trip_info.get('tripId')
                    if trip_id:
                        # Alert entities data
                        entities.append({
                            'trip_id': trip_id,
                            'alert_id': alert_id
                        })

                cause = elt.get('alert', {}).get('cause', 'unknown')
                severity = elt.get('alert', {}).get('severityLevel', 'unknown')

                # Headers translations and descriptions (text)
                header_en = 'unknown'
                header_fr = 'unknown'
                description_en = 'unknown'
                description_fr = 'unknown'

                # Process header translations
                header_text = elt.get('alert', {}).get('headerText', {})
                if 'translation' in header_text:
                    for header in header_text['translation']:
                        if header.get('language') == 'en':
                            header_en = header.get('text', 'unknown')
                        elif header.get('language') == 'fr':
                            header_fr = header.get('text', 'unknown')

                # Process description translations
                description_text = elt.get('alert', {}).get('descriptionText', {})
                if 'translation' in description_text:
                    for description in description_text['translation']:
                        if description.get('language') == 'en':
                            description_en = description.get('text', 'unknown')
                        elif description.get('language') == 'fr':
                            description_fr = description.get('text', 'unknown')

                # Alerts data
                alerts.append({
                    'alert_id': alert_id,
                    'active_period_start': active_period_start,
                    'active_period_end': active_period_end,
                    'cause': cause,
                    'severity': severity,
                    'header_en': header_en,
                    'header_fr': header_fr,
                    'description_en': description_en,
                    'description_fr': description_fr
                })
                
            except (KeyError, TypeError) as e:
                print(f"Error processing service alert {elt.get('id', 'unknown')}: {e}")
                continue

        return alerts, entities

    # Ingestion functions
    def ingest_data(self, engine: PostgreEngine, table_name:str, data:List[dict]) -> None:
        """Ingest data into a PostgreSQL table with upsert functionality"""
        if not data:
            return
            
        columns = list(data[0].keys())
        placeholders = ', '.join(['%s'] * len(columns))
        update_clause = ', '.join([f"{col} = EXCLUDED.{col}" for col in columns])
        
        # Query with conflict resolution - update on conflict
        query = f"""
        INSERT INTO {table_name} ({', '.join(columns)}) 
        VALUES ({placeholders}) 
        ON CONFLICT DO UPDATE SET {update_clause}
        """
        
        # Convert list of dicts to list of tuples for batch insertion
        params_list = [tuple(row.values()) for row in data]
        
        # Execute batch query
        engine.execute_batch_query(query, params_list)
        print(f"Processed {len(data)} records for {table_name} (inserted or updated)")

    # Main function (pipeline)
    def run(self) -> None:
        """Run the consumer"""
        print("Setting topics config to delete old messages")
        self.set_topic_config('gtfs-rt-tu')
        self.set_topic_config('gtfs-rt-sa')

        print("Starting message consumption")
        while True:
            trip_updates = []
            stop_time_updates = []
            alerts = []
            entities = []
            
            # Get data from Kafka
            try:
                tu_data = self.consume_messages(self.trip_update_consumer)
                sa_data = self.consume_messages(self.service_alert_consumer)
                print(f"Consumed {len(tu_data)} trip updates and {len(sa_data)} service alerts")
            except Exception as e:
                print(f"Error consuming messages: {e}")
                time.sleep(60)
                continue
            except KeyboardInterrupt:
                print("Stopping message consumption by keyboard interrupt")
                self.close_consumer(self.trip_update_consumer)
                self.close_consumer(self.service_alert_consumer)
                break
            else:
                # Transform data
                if tu_data or sa_data:
                    print("Processing messages")
                    if tu_data:
                        trip_updates, stop_time_updates = self.decompose_tu_data(tu_data)

                    if sa_data:
                        alerts, entities = self.decompose_sa_data(sa_data)

            # Ingest data in DB
            if trip_updates or stop_time_updates or alerts or entities:
                try:
                    with PostgreEngine(host = self.var_dict['POSTGRES_HOST'],
                                     port = self.var_dict['POSTGRES_PORT'],
                                     db = self.var_dict['POSTGRES_DB'],
                                     user = self.var_dict['POSTGRES_USER'],
                                     password = self.var_dict['POSTGRES_PASSWORD']) as engine:
                        
                        if trip_updates:
                            print(f"Ingesting {len(trip_updates)} trip updates")
                            self.ingest_data(engine, 'trip_updates', trip_updates)
                        if stop_time_updates:
                            print(f"Ingesting {len(stop_time_updates)} stop time updates")
                            self.ingest_data(engine, 'stop_time_updates', stop_time_updates)
                        if alerts:
                            print(f"Ingesting {len(alerts)} alerts")
                            self.ingest_data(engine, 'alerts', alerts)
                        if entities:
                            print(f"Ingesting {len(entities)} alert entities")
                            self.ingest_data(engine, 'alert_entities', entities)
                        
                        # Commit all insertions
                        engine.commit()
                        print("All data committed successfully")
                        
                except Exception as e:
                    print(f"Error during data ingestion: {e}")
                    continue
                finally:
                    # Sleep for 5 minute to avoid consuming messages too fast
                    time.sleep(300)

if __name__ == "__main__":
    # Fetch data sources URL
    with open(DATA_SOURCES_FILEPATH, 'r') as f:
        data_sources = json.load(f)

        var_dict = {
            'KAFKA_BROKERS': data_sources['kafka_brokers'],
            'POSTGRES_HOST': data_sources['postgres_host'],
            'POSTGRES_PORT': data_sources['postgres_port'],
            'POSTGRES_DB': data_sources['postgres_db'],
            'POSTGRES_USER': read_secret_or_env('postgres_user', 'POSTGRES_USER'),
            'POSTGRES_PASSWORD': read_secret_or_env('postgres_password', 'POSTGRES_PASSWORD')
        }
    del data_sources

    # Consumer engine
    engine = GTFSConsumer(var_dict)
    engine.run()
