import pytest
from redis.exceptions import RedisError, ConnectionError
from unittest.mock import patch, MagicMock

from src.producer.RedisEngine import RedisEngine


@pytest.fixture
def redis_mock():
    with patch("src.producer.RedisEngine.redis.Redis") as mock_redis:
        yield mock_redis


def test_connection_success(redis_mock):
    instance = MagicMock()
    redis_mock.return_value = instance
    instance.ping.return_value = True

    engine = RedisEngine(host="localhost", port=6379)

    assert engine.conn is not None
    instance.ping.assert_called_once()


def test_connection_failure(redis_mock):
    redis_mock.return_value.ping.side_effect = ConnectionError("Connection error")
    engine = RedisEngine(host="localhost", port=6379)

    assert engine.conn is None


def test_set_key_success(redis_mock):
    instance = MagicMock()
    redis_mock.return_value = instance
    instance.ping.return_value = True

    engine = RedisEngine(host="localhost", port=6379)
    engine.set("test_key", "value", 60)

    instance.set.assert_called_with("test_key", "value", 60)


def test_set_key_no_connection(redis_mock):
    instance = MagicMock()
    instance.ping.side_effect = RedisError("Connection error")
    redis_mock.return_value = instance

    engine = RedisEngine(host="localhost", port=6379)
    engine.set("key", "value", 60)

    assert engine.conn is None



def test_exists_key_found(redis_mock):
    instance = MagicMock()
    redis_mock.return_value = instance
    instance.ping.return_value = True
    instance.exists.return_value = 1

    engine = RedisEngine(host="localhost", port=6379)
    result = engine.exists("test_key")

    assert result is True
    instance.exists.assert_called_with("test_key")


def test_exists_key_not_found(redis_mock):
    instance = MagicMock()
    redis_mock.return_value = instance
    instance.ping.return_value = True
    instance.exists.return_value = 0

    engine = RedisEngine(host="localhost", port=6379)
    result = engine.exists("unknown_key")

    assert result is False


def test_get_key_success(redis_mock):
    instance = MagicMock()
    redis_mock.return_value = instance
    instance.ping.return_value = True
    instance.get.return_value = "value"

    engine = RedisEngine(host="localhost", port=6379)
    result = engine.get_key("test_key")

    assert result == "value"
    instance.get.assert_called_with("test_key")


def test_get_key_failure(redis_mock):
    instance = MagicMock()
    instance.ping.return_value = True
    instance.get.side_effect = RedisError("Some error")
    redis_mock.return_value = instance

    engine = RedisEngine(host="localhost", port=6379)
    result = engine.get_key("test_key")

    assert result is False