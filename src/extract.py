# src/extract.py
"""
Extract GTFS data from SNCF API and send them to Kafka
"""

from google.transit import gtfs_realtime_pb2
import json
import requests



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
            entity_data['trip_update'] = entity.trip_update
            all_data.append(entity_data)
    return all_ids, all_data


def extract_ids_and_service_alerts(feed: gtfs_realtime_pb2.FeedMessage) -> list[dict]:
    """
    Extract IDs and service alerts from GTFS data
    """
    all_ids = []
    all_data = []
    if feed:
        for entity in feed.entity:
            entity_data = {}
            entity_data['id'] = entity.id
            all_ids.append(entity.id)
            entity_data['service_alert'] = entity.service_alert
            all_data.append(entity_data)
    return all_ids, all_data

def remove_existing_ids(ids: list[str], existing_ids: list[str]) -> list[str]:
    pass


if __name__ == "__main__":
    # Fetch data sources URL
    with open('src/data_sources.json', 'r') as f:
        data_sources = json.load(f)
        GTFS_RT_TU_URL = data_sources['gtfs_rt_tu_url']
        GTFS_RT_SA_URL = data_sources['gtfs_rt_sa_url']

    # GTFS RT Trip Updates
    tu_feed = fetch_gtfs_rt(GTFS_RT_TU_URL)
    tu_ids, tu_data = extract_ids_and_trip_updates(tu_feed)







    # sa_feed = fetch_gtfs_rt(GTFS_RT_SA_URL)