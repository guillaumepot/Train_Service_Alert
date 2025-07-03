# src/gtfs-update/gtfs-update.py
"""
ETL Pipeline to update GTFS data in DB
"""

import json
import os
import pandas as pd
import requests
import zipfile

DATA_SOURCES_FILEPATH = os.getenv('DATA_SOURCES_FILEPATH', 'config/data_sources.json')



# EXTRACT
def download_gtfs_data(url: str) -> None:
    """
    Fetch GTFS files from source
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.content
    except Exception as e:
        raise e


def extract_data_from_zip(data: bytes) -> None:
    if not os.path.exists('tmp_gtfs'):
        os.makedirs('tmp_gtfs')
    with open('tmp_gtfs/raw_gtfs.zip', 'wb') as f:
        f.write(data)
    with zipfile.ZipFile('tmp_gtfs/raw_gtfs.zip', 'r') as zip_ref:
        zip_ref.extractall('tmp_gtfs')
    os.remove('tmp_gtfs/raw_gtfs.zip')
    return


def remove_tmp_files() -> None:
    for file in os.listdir('tmp_gtfs'):
        os.remove(os.path.join('tmp_gtfs', file))
    os.rmdir('tmp_gtfs')
    return


def load_df_dict() -> dict:
    df_dict = {}
    for file in os.listdir('tmp_gtfs'):
        if file.endswith('.txt'):
            df = pd.read_csv(f'tmp_gtfs/{file}')
            file_name = file.split('.')[0]
            df_dict[file_name] = df
    return df_dict


def pipeline_extract(url:str) -> dict:
    data = download_gtfs_data(url)
    extract_data_from_zip(data)
    df_dict = load_df_dict()
    remove_tmp_files()    
    return df_dict



# TRANSFORM
def clean_df(df: pd.DataFrame, actions:dict) -> pd.DataFrame:
    if 'drop_col' in actions.keys():
        df = df.drop(actions['drop_col'], axis = 1)

    if 'fillna' in actions.keys():
        df = df.fillna(actions['fillna'])

    return df


def pipeline_transform(df_dict: dict) -> dict:
    # Clean feed_info
    df_dict.pop('feed_info')
    # Clean calendar_dates
    df_dict.pop('calendar_dates')
    # Clean transfers
    df_dict.pop('transfers')

    # Clean stop_times
    actions = {
        'drop_col': ['stop_headsign', 'shape_dist_traveled']
    }
    df_dict['stop_times'] = clean_df(df_dict['stop_times'], actions = actions)

    # Clean routes
    actions = {
        'drop_col': ['route_desc', 'route_url', 'route_color', 'route_text_color']
    }
    df_dict['routes'] = clean_df(df_dict['routes'], actions = actions)

    # Clean  trips
    actions = {
        'drop_col': ['shape_id'],
        'fillna': {
            'direction_id': -1.0
        }
    }
    df_dict['trips'] = clean_df(df_dict['trips'], actions = actions)

    # Clean stops
    actions = {
        'drop_col': ['stop_desc', 'zone_id', 'stop_url'],
        'fillna': {
            'parent_station': "No_parent_station"
        }
    }
    df_dict['stops'] = clean_df(df_dict['stops'], actions = actions)

    return df_dict


# LOAD
def pipeline_load(df_dict: dict) -> None:
    pass





# ETL (main)
def main(url:str):
    df_dict = pipeline_extract(url)
    df_dict = pipeline_transform(df_dict)
    # Debug
    # for key, df in df_dict.items():
        # print(f'DF {key} size : {df.shape[0]}')
    pipeline_load(df_dict)


if __name__ == "__main__":
    # Fetch data sources URL
    with open(DATA_SOURCES_FILEPATH, 'r') as f:
        data_sources = json.load(f)
    GTFS_URL = data_sources['gtfs_url']
    del data_sources

    # Start pipeline
    main(GTFS_URL)