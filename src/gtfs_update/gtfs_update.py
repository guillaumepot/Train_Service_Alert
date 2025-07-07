# src/gtfs-update/gtfs-update.py
"""
ETL Pipeline to update GTFS data in DB
"""
import json
import os
import pandas as pd
import requests
import zipfile
from datetime import datetime, timedelta

from PostgreEngine import PostgreEngine

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
    """
    Extract all files from the zip file and save them in tmp_gtfs
    """
    if not os.path.exists('tmp_gtfs'):
        os.makedirs('tmp_gtfs')
    with open('tmp_gtfs/raw_gtfs.zip', 'wb') as f:
        f.write(data)
    with zipfile.ZipFile('tmp_gtfs/raw_gtfs.zip', 'r') as zip_ref:
        zip_ref.extractall('tmp_gtfs')
    os.remove('tmp_gtfs/raw_gtfs.zip')
    return


def remove_tmp_files() -> None:
    """
    Remove all files in tmp_gtfs
    """
    for file in os.listdir('tmp_gtfs'):
        os.remove(os.path.join('tmp_gtfs', file))
    os.rmdir('tmp_gtfs')
    return


def load_df_dict() -> dict:
    """
    Load all files in tmp_gtfs into a dictionary
    """
    df_dict = {}
    for file in os.listdir('tmp_gtfs'):
        if file.endswith('.txt'):
            df = pd.read_csv(f'tmp_gtfs/{file}')
            file_name = file.split('.')[0]
            df_dict[file_name] = df
    return df_dict


def pipeline_extract(url:str) -> dict:
    """
    Extract all files from the zip file and save them in tmp_gtfs, then load them into a dictionary and remove the tmp_gtfs folder
    """
    data = download_gtfs_data(url)
    extract_data_from_zip(data)
    df_dict = load_df_dict()
    remove_tmp_files()    
    return df_dict



# TRANSFORM
def convert_gtfs_time_to_timestamp(time_str):
    """
    Convert GTFS time format (HH:MM:SS) to PostgreSQL timestamp.
    GTFS times can exceed 24:00:00 to represent times after midnight.
    """
    if pd.isna(time_str) or time_str == '':
        return None
    
    try:
        # Parse the time string
        hours, minutes, seconds = map(int, time_str.split(':'))
        
        # Create base date (today for simplicity)
        base_date = datetime.now().date()
        
        # Handle times >= 24:00:00 (next day)
        if hours >= 24:
            days_offset = hours // 24
            hours = hours % 24
            base_date += timedelta(days=days_offset)
        
        # Create timestamp
        timestamp = datetime.combine(base_date, datetime.min.time()) + timedelta(
            hours=hours, minutes=minutes, seconds=seconds
        )
        
        return timestamp
    except (ValueError, AttributeError):
        return None


def convert_gtfs_time_to_time(time_str):
    """
    Convert GTFS time format (HH:MM:SS) to PostgreSQL time format.
    GTFS times can exceed 24:00:00 to represent times after midnight.
    For times >= 24:00:00, convert to equivalent time on next day (e.g., 24:09:00 -> 00:09:00).
    """
    if pd.isna(time_str) or time_str == '':
        return None
    
    try:
        # Parse the time string
        hours, minutes, seconds = map(int, time_str.split(':'))
        
        # Handle times >= 24:00:00 (convert to equivalent time)
        if hours >= 24:
            hours = hours % 24
        
        # Create time object
        time_obj = datetime.min.time().replace(hour=hours, minute=minutes, second=seconds)
        
        return time_obj
    except (ValueError, AttributeError):
        return None


def clean_df(df: pd.DataFrame, actions:dict) -> pd.DataFrame:
    """
    Clean the dataframe based on the actions dictionary
    """
    if 'drop_col' in actions.keys():
        df = df.drop(actions['drop_col'], axis = 1)

    if 'fillna' in actions.keys():
        df = df.fillna(actions['fillna'])

    return df


def pipeline_transform(df_dict: dict) -> dict:
    """
    Clean the dataframe based on the actions dictionary
    """
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
    
    # Convert GTFS time format to PostgreSQL time format for stop_times
    if 'arrival_time' in df_dict['stop_times'].columns:
        df_dict['stop_times']['arrival_time'] = df_dict['stop_times']['arrival_time'].apply(convert_gtfs_time_to_time)
    if 'departure_time' in df_dict['stop_times'].columns:
        df_dict['stop_times']['departure_time'] = df_dict['stop_times']['departure_time'].apply(convert_gtfs_time_to_time)

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
def pipeline_load(df_dict: dict, pg_vars: dict) -> None:
    """
    Load all dataframes into the database
    """
    # insertion order based on foreign key dependencies
    insertion_order = ['agency', 'stops', 'routes', 'trips', 'stop_times']
    
    # Define primary keys for each table (Avoid error on duplicates)
    primary_keys = {
        'agency': ['agency_id'],
        'stops': ['stop_id'],
        'routes': ['route_id'],
        'trips': ['trip_id'],
        'stop_times': ['trip_id', 'stop_sequence']
    }
    
    with PostgreEngine(pg_vars['POSTGRES_HOST'], pg_vars['POSTGRES_PORT'], pg_vars['POSTGRES_DB'], pg_vars['POSTGRES_USER'], pg_vars['POSTGRES_PASSWORD']) as pg:
        
        try:
            # Insert tables in the correct order
            for table_name in insertion_order:
                if table_name not in df_dict:
                    print(f"Table {table_name} not found in data dictionary, skipping")
                    continue
                
                df = df_dict[table_name]
                if len(df) == 0:
                    print(f"Skipping empty dataframe for table: {table_name}")
                    continue
                
                # Get primary key columns for this table
                primary_key_columns = primary_keys[table_name]
                primary_key_column = ', '.join(primary_key_columns)
                
                # Generate update assignments for non-primary key columns
                non_pk_columns = [col for col in df.columns if col not in primary_key_columns]
                update_assignments = ', '.join([f"{col} = EXCLUDED.{col}" for col in non_pk_columns])
                
                # INSERT data query
                columns = ', '.join(df.columns)
                placeholders = ', '.join(['%s'] * len(df.columns))
                insert_query = f"""
                    INSERT INTO {table_name} ({columns}) VALUES ({placeholders})
                    ON CONFLICT ({primary_key_column}) DO UPDATE SET
                    {update_assignments}
                """
                # Convert dataframe -> list of tuples for batch insert
                values_list = [tuple(row) for row in df.to_numpy()]
                
                # Execute insert
                print(f"Inserting {len(values_list)} rows into {table_name}")
                pg.execute_batch_query(insert_query, values_list)
                
            pg.commit()
            print("All data successfully loaded into database")
            
        except Exception as e:
            pg.rollback()
            print(f"Error during data loading: {e}")
            raise e
        

# ETL (main)
def main(variables: dict):
    """
    Apply the ETL pipeline to the GTFS data
    """
    df_dict = pipeline_extract(variables['GTFS_URL'])
    df_dict = pipeline_transform(df_dict)
    # Debug
    # for key, df in df_dict.items():
        # print(f'DF {key} size : {df.shape[0]}')
    pipeline_load(df_dict, variables)


if __name__ == "__main__":
    # Fetch data sources URL
    with open(DATA_SOURCES_FILEPATH, 'r') as f:
        data_sources = json.load(f)

    var_dict = {
        'GTFS_URL': data_sources['gtfs_url'],
        'POSTGRES_HOST': data_sources['postgres_host'],
        'POSTGRES_PORT': data_sources['postgres_port'],
        'POSTGRES_DB': data_sources['postgres_db'],
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD')
    }
    del data_sources

    # Start pipeline
    main(var_dict)