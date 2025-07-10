# tests/test_gtfs_update.py
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/gtfs_update')))
gtfs_update = importlib.import_module('gtfs_update')

def test_pipeline_extract(monkeypatch):
    monkeypatch.setattr(gtfs_update, 'download_gtfs_data', lambda url: b'data')
    monkeypatch.setattr(gtfs_update, 'extract_data_from_zip', lambda data: None)
    monkeypatch.setattr(gtfs_update, 'load_df_dict', lambda: {'foo': pd.DataFrame({'a': [1,2]})})
    monkeypatch.setattr(gtfs_update, 'remove_tmp_files', lambda: None)
    result = gtfs_update.pipeline_extract('fake_url')
    assert 'foo' in result
    assert isinstance(result['foo'], pd.DataFrame)

def test_pipeline_transform():
    df_dict = {
        'feed_info': pd.DataFrame(),
        'calendar_dates': pd.DataFrame(),
        'transfers': pd.DataFrame(),
        'stop_times': pd.DataFrame({'arrival_time': ['12:00:00'], 'departure_time': ['13:00:00'], 'stop_headsign': ['x'], 'shape_dist_traveled': [1]}),
        'routes': pd.DataFrame({'route_desc': ['desc'], 'route_url': ['url'], 'route_color': ['color'], 'route_text_color': ['text'], 'id':[1]}),
        'trips': pd.DataFrame({'shape_id': [1], 'direction_id': [None]}),
        'stops': pd.DataFrame({'stop_desc': ['desc'], 'zone_id': [1], 'stop_url': ['url'], 'parent_station': [None]})
    }
    result = gtfs_update.pipeline_transform(df_dict)
    assert 'feed_info' not in result
    assert 'calendar_dates' not in result
    assert 'transfers' not in result
    assert 'stop_headsign' not in result['stop_times'].columns
    assert 'route_desc' not in result['routes'].columns
    assert 'shape_id' not in result['trips'].columns
    assert result['stops']['parent_station'].iloc[0] == 'No_parent_station'

def test_pipeline_load():
    df_dict = {
        'agency': pd.DataFrame({'id': [1]}),
        'stops': pd.DataFrame({'id': [1]}),
        'routes': pd.DataFrame({'id': [1]}),
        'trips': pd.DataFrame({'id': [1]}),
        'stop_times': pd.DataFrame({'id': [1]})
    }
    pg_vars = {
        'POSTGRES_HOST': 'h',
        'POSTGRES_PORT': 'p',
        'POSTGRES_DB': 'd',
        'POSTGRES_USER': 'u',
        'POSTGRES_PASSWORD': 'pw'
    }
    with patch('gtfs_update.PostgreEngine') as MockPg:
        mock_pg = MagicMock()
        MockPg.return_value.__enter__.return_value = mock_pg
        gtfs_update.pipeline_load(df_dict, pg_vars)
        assert mock_pg.execute_batch_query.call_count == 5
        mock_pg.commit.assert_called_once() 