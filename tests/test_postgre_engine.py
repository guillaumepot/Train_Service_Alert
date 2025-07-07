# tests/test_postgre_engine.py

import pytest
from unittest.mock import patch, MagicMock
from src.gtfs_update.PostgreEngine import PostgreEngine

@pytest.fixture
def db_params():
    return {
        'host': 'localhost',
        'port': '5432',
        'db': 'testdb',
        'user': 'testuser',
        'password': 'testpass'
    }

@patch('src.gtfs_update.PostgreEngine.psycopg.connect')
def test_connect_success(mock_connect, db_params):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    engine = PostgreEngine(**db_params)
    engine.connect()
    mock_connect.assert_called_once_with(
        host='localhost', port='5432', user='testuser', password='testpass', dbname='testdb'
    )
    assert hasattr(engine, 'conn')
    assert hasattr(engine, 'cursor')

@patch('src.gtfs_update.PostgreEngine.psycopg.connect', side_effect=Exception('fail'))
def test_connect_failure(mock_connect, db_params):
    engine = PostgreEngine(**db_params)
    with pytest.raises(Exception):
        engine.connect()

@patch('src.gtfs_update.PostgreEngine.psycopg.connect')
def test_close_success(mock_connect, db_params):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    engine = PostgreEngine(**db_params)
    engine.connect()
    engine.close()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

@patch('src.gtfs_update.PostgreEngine.psycopg.connect')
def test_commit_success(mock_connect, db_params):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    engine = PostgreEngine(**db_params)
    engine.connect()
    engine.commit()
    mock_conn.commit.assert_called_once()

@patch('src.gtfs_update.PostgreEngine.psycopg.connect')
def test_rollback_success(mock_connect, db_params):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    engine = PostgreEngine(**db_params)
    engine.connect()
    engine.rollback()
    mock_conn.rollback.assert_called_once()

@patch('src.gtfs_update.PostgreEngine.psycopg.connect')
def test_execute_query_success(mock_connect, db_params):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    engine = PostgreEngine(**db_params)
    engine.connect()
    engine.execute_query('SELECT 1', (1,))
    mock_cursor.execute.assert_called_once_with('SELECT 1', (1,))

@patch('src.gtfs_update.PostgreEngine.psycopg.connect')
def test_execute_batch_query_success(mock_connect, db_params):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn
    engine = PostgreEngine(**db_params)
    engine.connect()
    engine.execute_batch_query('INSERT INTO t VALUES (%s)', [(1,), (2,)])
    mock_cursor.executemany.assert_called_once_with('INSERT INTO t VALUES (%s)', [(1,), (2,)]) 