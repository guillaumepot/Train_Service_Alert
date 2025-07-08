import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Ensure src/consumer is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/consumer')))
from consumer import GTFSConsumer

# Patch KafkaConsumer and KafkaAdminClient for all tests
def pytest_configure():
    patcher1 = patch('consumer.KafkaConsumer', MagicMock())
    patcher2 = patch('consumer.KafkaAdminClient', MagicMock())
    patcher1.start()
    patcher2.start()
    pytest.kafka_patchers = (patcher1, patcher2)

def pytest_unconfigure():
    for patcher in getattr(pytest, 'kafka_patchers', []):
        patcher.stop()

@pytest.fixture(autouse=True)
def mock_kafka(monkeypatch):
    # Patch again for test functions (in case)
    monkeypatch.setattr('consumer.KafkaConsumer', MagicMock())
    monkeypatch.setattr('consumer.KafkaAdminClient', MagicMock())

@pytest.fixture
def var_dict():
    return {
        'KAFKA_BROKERS': 'localhost:9092',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'testdb',
        'POSTGRES_USER': 'user',
        'POSTGRES_PASSWORD': 'pass'
    }

def test_unix_to_datetime_valid(var_dict):
    consumer = GTFSConsumer(var_dict)
    dt = consumer.unix_to_datetime(1609459200)  # 2021-01-01 00:00:00 UTC
    assert dt.year == 2021 and dt.month == 1 and dt.day == 1

def test_unix_to_datetime_none(var_dict):
    consumer = GTFSConsumer(var_dict)
    assert consumer.unix_to_datetime(None) is None

def test_format_time_str(var_dict):
    consumer = GTFSConsumer(var_dict)
    assert consumer.format_time('12:34:56') == '12:34:56'

def test_format_time_unix(var_dict):
    consumer = GTFSConsumer(var_dict)
    # 1609459260 = 2021-01-01 00:01:00 UTC
    assert consumer.format_time(1609459260) == '00:01:00'

def test_format_date_str(var_dict):
    consumer = GTFSConsumer(var_dict)
    assert consumer.format_date('2021-01-01') == '2021-01-01'

def test_format_date_yyyymmdd(var_dict):
    consumer = GTFSConsumer(var_dict)
    assert consumer.format_date('20210101') == '2021-01-01'

def test_decompose_tu_data_empty(var_dict):
    consumer = GTFSConsumer(var_dict)
    trip_updates, stop_time_updates = consumer.decompose_tu_data([])
    assert trip_updates == []
    assert stop_time_updates == []

def test_decompose_sa_data_empty(var_dict):
    consumer = GTFSConsumer(var_dict)
    alerts, entities = consumer.decompose_sa_data([])
    assert alerts == []
    assert entities == []

def test_ingest_data_no_data(var_dict):
    consumer = GTFSConsumer(var_dict)
    engine = MagicMock()
    consumer.ingest_data(engine, 'table', [])
    engine.execute_batch_query.assert_not_called()

def test_ingest_data_with_data(var_dict):
    consumer = GTFSConsumer(var_dict)
    engine = MagicMock()
    data = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
    consumer.ingest_data(engine, 'table', data)
    engine.execute_batch_query.assert_called_once()
    args, kwargs = engine.execute_batch_query.call_args
    assert args[0] == 'INSERT INTO table (a, b) VALUES (%s, %s)'
    assert args[1] == [(1, 2), (3, 4)]

def test_get_consumer_creates_kafka_consumer(var_dict):
    consumer = GTFSConsumer(var_dict)
    with patch('consumer.KafkaConsumer') as mock_kafka:
        mock_kafka.return_value = MagicMock()
        c = consumer.get_consumer('topic', 'group')
        assert mock_kafka.called
        assert c == mock_kafka.return_value

def test_consume_messages_returns_data(var_dict):
    consumer = GTFSConsumer(var_dict)
    fake_consumer = MagicMock()
    fake_consumer.poll.return_value = {('topic', 0): [MagicMock(value={'foo': 'bar'})]}
    result = consumer.consume_messages(fake_consumer)
    assert result == [{'foo': 'bar'}]

def test_close_consumer_calls_close(var_dict):
    consumer = GTFSConsumer(var_dict)
    fake_consumer = MagicMock()
    consumer.close_consumer(fake_consumer)
    fake_consumer.close.assert_called_once()

def test_set_topic_config_calls_admin_client(var_dict):
    consumer = GTFSConsumer(var_dict)
    with patch('consumer.KafkaAdminClient') as mock_admin:
        mock_admin.return_value = MagicMock()
        consumer.set_topic_config('topic', {'retention.ms': '1000'})
        assert mock_admin.called 