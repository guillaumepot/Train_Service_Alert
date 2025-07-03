import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/producer')))
from unittest.mock import patch
from src.producer.producer import fetch_gtfs_rt, extract_ids_and_trip_updates, is_already_sent

# --- fetch_gtfs_rt ---
def test_fetch_gtfs_rt_returns_none_on_error():
    with patch('src.producer.producer.requests.get', side_effect = Exception('fail')):
        result = fetch_gtfs_rt('http://bad.url')
        assert result is None

# --- extract_ids_and_trip_updates ---
class FakeEntity:
    def __init__(self, id, has_trip_update = False, has_alert = False):
        self.id = id
        self._has_trip_update = has_trip_update
        self._has_alert = has_alert
    def HasField(self, field):
        return (field == 'trip_update' and self._has_trip_update) or (field == 'alert' and self._has_alert)
    @property
    def trip_update(self):
        return {'foo': 'bar'}
    @property
    def alert(self):
        return {'baz': 'qux'}
    def __str__(self):
        return f"FakeEntity({self.id})"

class FakeFeed:
    def __init__(self, entities):
        self.entity = entities

def test_extract_ids_and_trip_updates_trip_update(monkeypatch):
    # Patch MessageToDict to just return the dict
    monkeypatch.setattr('src.producer.producer.MessageToDict', lambda x: x)
    feed = FakeFeed([FakeEntity('1', has_trip_update=True)])
    ids, data = extract_ids_and_trip_updates(feed)
    assert ids == ['1']
    assert data[0]['id'] == '1'
    assert 'trip_update' in data[0]

def test_extract_ids_and_trip_updates_alert(monkeypatch):
    monkeypatch.setattr('src.producer.producer.MessageToDict', lambda x: x)
    feed = FakeFeed([FakeEntity('2', has_alert=True)])
    ids, data = extract_ids_and_trip_updates(feed)
    assert ids == ['2']
    assert data[0]['id'] == '2'
    assert 'alert' in data[0]

def test_extract_ids_and_trip_updates_empty():
    feed = FakeFeed([])
    ids, data = extract_ids_and_trip_updates(feed)
    assert ids == []
    assert data == []

# --- is_already_sent ---
class DummyRedis:
    def __init__(self, exists_return = False):
        self._exists = exists_return
        self.set_calls = []
    def exists(self, key):
        return self._exists
    def set(self, key, value, delay):
        self.set_calls.append((key, value, delay))


def test_is_already_sent_true():
    redis = DummyRedis(exists_return=True)
    assert is_already_sent(redis, 'type', 'id') is True
    assert redis.set_calls == []

def test_is_already_sent_false():
    redis = DummyRedis(exists_return=False)
    assert is_already_sent(redis, 'type', 'id', delay=123) is False
    assert redis.set_calls == [('type_id', '1', 123)]



