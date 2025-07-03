# src/producer/extract.py
"""
Extract GTFS data from SNCF API and send them to Kafka
"""
import concurrent.futures
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from kafka import KafkaProducer
import json
import os
import requests
import time
from typing import List

from RedisEngine import RedisEngine


DATA_SOURCES_FILEPATH = os.getenv('DATA_SOURCES_FILEPATH', 'config/data_sources.json')



def fetch_gtfs_rt(url:str) -> gtfs_realtime_pb2.FeedMessage:
    """
    Fetch GTFS data from SNCF API

    Args:
        url (str): The URL of the SNCF API

    Returns:
        gtfs_realtime_pb2.FeedMessage: The GTFS data
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed
    except Exception as e:
        print(e)
        return None


def extract_ids_and_trip_updates(feed: gtfs_realtime_pb2.FeedMessage) -> list[dict]:
    """
    Extract IDs and trip updates from GTFS data
    """
    all_ids = []
    all_data = []
    if feed:
        for entity in feed.entity:
            entity_data = {}
            entity_data['id'] = entity.id
            all_ids.append(entity.id)
            # Convert protobuf trip_update to dictionary for JSON serialization (Kafka messages)
            if entity.HasField('trip_update'):
                entity_data['trip_update'] = MessageToDict(entity.trip_update)
            elif entity.HasField('alert'):
                entity_data['alert'] = MessageToDict(entity.alert)
            else:
                print(f"Unknown entity type: {entity}")
                continue
            all_data.append(entity_data)
    return all_ids, all_data


def is_already_sent(redis_engine: RedisEngine, type:str, id: str, delay: int = 36000) -> bool:
    """
    Check if the data has already been sent to Kafka during the last {delay} seconds (Redis cache check)
    """
    if redis_engine.exists(f"{type}_{id}"):
        return True
    redis_engine.set(f"{type}_{id}", "1", delay)
    return False


def send_to_kafka(brokers, topic:str, data:list[dict]):
    """
    Send data to Kafka
    """
    if not data:
        print(f"No new data to send to topic {topic}")
        return
        
    producer = KafkaProducer(bootstrap_servers = brokers, 
                             value_serializer=lambda v: json.dumps(v).encode("utf-8"))

    sent_count = 0
    failed_count = 0
    
    for record in data:
        try:
            producer.send(topic, record)
            sent_count += 1
        except Exception as e:
            print(f"Error sending individual message to Kafka: {e}")
            failed_count += 1
    
    # Ensure all messages are sent before closing
    producer.flush()
    producer.close()
    
    print(f"Sent {sent_count} messages to topic {topic}, {failed_count} failed")
    return


def process_feed_data(url: str, redis_type: str, kafka_topic: str, redis_engine: RedisEngine, kafka_brokers: List[str]) -> None:
    """
    Process GTFS feed (TU or SA)
    
    Args:
        url: The GTFS feed URL
        redis_type: Type for Redis keys ("trip_update" or "service_alert")
        kafka_topic: Kafka topic to send data to
        redis_engine: Redis engine instance
        kafka_brokers: List of Kafka brokers
    """
    # Fetch feed data
    feed = fetch_gtfs_rt(url)
    if not feed:
        print(f"Failed to fetch data from {url}")
        return
    
    _, all_data = extract_ids_and_trip_updates(feed)
    print(f'Fetched {len(all_data)} items from {kafka_topic}')
    
    # Filter out already sent data
    filtered_data = []
    for item in all_data:
        if not is_already_sent(redis_engine, redis_type, item['id']):
            filtered_data.append(item)
    
    print(f'After filtering: {len(filtered_data)} new items for {kafka_topic}')
    
    # Send to Kafka
    send_to_kafka(brokers = kafka_brokers, topic = kafka_topic, data = filtered_data)


def main():
    """
    Main function to extract GTFS data from SNCF API and send them to Kafka
    """
    # Parallel processing of TU and SA feeds
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        tu_future = executor.submit(
            process_feed_data,
            GTFS_RT_TU_URL,
            "trip_update", 
            'gtfs-rt-tu',
            redis_engine,
            KAFKA_BROKERS
        )
        
        sa_future = executor.submit(
            process_feed_data,
            GTFS_RT_SA_URL,
            "service_alert",
            'gtfs-rt-sa', 
            redis_engine,
            KAFKA_BROKERS
        )
        
        # Wait for both tasks to complete
        concurrent.futures.wait([tu_future, sa_future])
        
        try:
            tu_future.result()
        except Exception as e:
            print(f"Error processing trip updates: {e}")
            
        try:
            sa_future.result()
        except Exception as e:
            print(f"Error processing service alerts: {e}")


if __name__ == "__main__":
    # Fetch data sources URL
    with open(DATA_SOURCES_FILEPATH, 'r') as f:
        data_sources = json.load(f)
    GTFS_RT_TU_URL = data_sources['gtfs_rt_tu_url']
    GTFS_RT_SA_URL = data_sources['gtfs_rt_sa_url']
    REDIS_HOST = data_sources['redis_host']
    REDIS_PORT = data_sources['redis_port']
    KAFKA_BROKERS = data_sources['kafka_brokers']
    del data_sources

    # Wait to let Kafka & Redis to be ready in case of restart
    time.sleep(60)

    # Redis engine 
    redis_engine = RedisEngine(host = REDIS_HOST, port = REDIS_PORT)

    # Redis engine 
    redis_engine = RedisEngine(host = REDIS_HOST, port = REDIS_PORT)

    # Start extraction loop
    while True:
        main()
        # Wait
        time.sleep(60)