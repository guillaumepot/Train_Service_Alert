# src/consumer/consumer.py
"""
Extract GTFS RT messages from Kafka, process them and save them to the database
"""
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, ConfigResource, ConfigResourceType
import json
import os
import pandas as pd
import time
from typing import List



DATA_SOURCES_FILEPATH = os.getenv('DATA_SOURCES_FILEPATH', 'config/data_sources.json')


class GTFSConsumer:
    def __init__(self, var_dict:dict):
        self.var_dict = var_dict
        self.trip_update_consumer = self.get_consumer('gtfs-rt-tu', 'gtfs-rt-consumer')
        self.service_alert_consumer = self.get_consumer('gtfs-rt-sa', 'gtfs-rt-consumer')

    def get_consumer(self, topic:str, group_id:str) -> KafkaConsumer:
        consumer = KafkaConsumer(topic,
                                 bootstrap_servers = self.var_dict['KAFKA_BROKERS'],
                                 auto_offset_reset = 'earliest',
                                 enable_auto_commit = True,
                                 group_id = group_id,
                                 value_deserializer = lambda m: json.loads(m.decode('utf-8'))
                                    )
        return consumer


    def consume_messages(self, consumer: KafkaConsumer, timeout_ms:int = 1000, max_messages:int = 1000) -> List[dict]:
        consumed_data = []
        messages = consumer.poll(timeout_ms=timeout_ms, max_records=max_messages)
        for topic_partition, records in messages.items():
            for message in records:
                message_data = {
                    'payload': message.value,
                    'timestamp': message.timestamp,
                    'offset': message.offset,
                    'partition': message.partition,
                    'topic': message.topic
                }
                consumed_data.append(message_data)
        return consumed_data

    def close_consumer(self, consumer: KafkaConsumer) -> None:
        consumer.close()

    def set_topic_config(self, topic:str, config:dict = None) -> None:
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


    # self.postgres_host = var_dict['POSTGRES_HOST']
    # self.postgres_port = var_dict['POSTGRES_PORT']
    # self.postgres_db = var_dict['POSTGRES_DB']
    # self.postgres_user = var_dict['POSTGRES_USER']
    # self.postgres_password = var_dict['POSTGRES_PASSWORD']



    def run(self):
        print("Setting topics config to delete old messages")
        self.set_topic_config('gtfs-rt-tu')
        self.set_topic_config('gtfs-rt-sa')

        print("Starting message consumption")
        while True:
            try:
                tu_data = self.consume_messages(self.trip_update_consumer)
                sa_data = self.consume_messages(self.service_alert_consumer)
                print(f"Consumed {len(tu_data)} trip updates and {len(sa_data)} service alerts")
            except Exception as e:
                print(f"Error consuming messages: {e}")
                time.sleep(10)
            except KeyboardInterrupt:
                print("Stopping message consumption by keyboard interrupt")
                self.close_consumer(self.trip_update_consumer)
                self.close_consumer(self.service_alert_consumer)
                break
            else:
                if tu_data or sa_data:
                    trip_updates = []
                    all_stop_time_updates = []
                    for elt in tu_data:
                        try:
                            payload = elt['payload']
                            
                            if 'header' in payload and 'timestamp' in payload['header']:
                                feed_timestamp = payload['header']['timestamp']
                            else:
                                feed_timestamp = elt['timestamp']
                            
                            trip_id = payload['trip_update']['trip']['tripId']
                            trip_start_time = payload['trip_update']['trip']['startTime']
                            trip_start_date = payload['trip_update']['trip']['startDate']

                            trip_updates.append({
                                'trip_id': trip_id,
                                'trip_start_time': trip_start_time,
                                'trip_start_date': trip_start_date
                            })

                            # Process stop time updates for this trip
                            stop_sequence = 0
                            if 'stopTimeUpdate' in payload:
                                for stop_time_update in payload['stopTimeUpdate']:
                                    stop_index = stop_sequence
                                    stop_sequence += 1

                                    if 'arrival' in stop_time_update:
                                        arrival_time = stop_time_update['arrival']['time']
                                        arrival_delay = stop_time_update['arrival']['delay']
                                    else:
                                        arrival_time = None
                                        arrival_delay = None

                                    if 'departure' in stop_time_update:
                                        departure_time = stop_time_update['departure']['time']
                                        departure_delay = stop_time_update['departure']['delay']
                                    else:
                                        departure_time = None
                                        departure_delay = None

                                    all_stop_time_updates.append({
                                        'feed_timestamp': feed_timestamp,
                                        'trip_id': trip_id,
                                        'stop_index': stop_index,
                                        'stop_id': stop_time_update['stopId'],
                                        'arrival_time': arrival_time,
                                        'departure_time': departure_time,
                                        'arrival_delay': arrival_delay,
                                        'departure_delay': departure_delay
                                    })
                        
                        except KeyError as e:
                            print(f"ERROR: Missing key {e} in trip update data.")
                            print(f"Available payload keys: {list(elt.get('payload', {}).keys())}")
                            continue
                        except Exception as e:
                            print(f"ERROR: Unexpected error processing trip update: {e}")
                            continue

                    trip_updates_df = pd.DataFrame(trip_updates)
                    stop_time_updates_df = pd.DataFrame(all_stop_time_updates)


                    print(trip_updates_df.head()) # DEV
                    print(stop_time_updates_df.head()) # DEV
                else:
                    # No messages available, sleep 1 minute
                    time.sleep(30)






if __name__ == "__main__":
    # Fetch data sources URL
    with open(DATA_SOURCES_FILEPATH, 'r') as f:
        data_sources = json.load(f)

        var_dict = {
            # 'KAFKA_BROKERS': data_sources['kafka_brokers'],
            'POSTGRES_HOST': data_sources['postgres_host'],
            'POSTGRES_PORT': data_sources['postgres_port'],
            'POSTGRES_DB': data_sources['postgres_db'],
            'POSTGRES_USER': os.getenv('POSTGRES_USER'),
            'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD')
        }
    del data_sources

    var_dict['KAFKA_BROKERS'] = ["localhost:9092", "localhost:9093"] # DEV


    # Consumer engine
    engine = GTFSConsumer(var_dict)
    engine.run()