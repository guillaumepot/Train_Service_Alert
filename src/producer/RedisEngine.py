#src/producer/RedisEngine.py

import redis
from redis.exceptions import RedisError, ConnectionError, TimeoutError


class RedisEngine():
    def __init__(self, host:str, port:int, health_check_interval:int = 30, decode_responses: bool = True):
        self.host = host
        self.port = port
        self.health_check_interval = health_check_interval
        self.decode_responses = decode_responses
        self.conn = None
        self._connect()

    def _connect(self):
        try:
            self.conn = redis.Redis(
                host=self.host,
                port=self.port,
                decode_responses=self.decode_responses,
                health_check_interval=self.health_check_interval
            )
            self.conn.ping()
            print("Redis connection established.")
        except (ConnectionError, TimeoutError, RedisError) as e:
            self.conn = None
            print(f"Redis connection failed: {e}")

    def _reconnect_if_needed(self):
        if self.conn is None:
            print("Attempting Redis reconnection...")
            self._connect()


    def set(self, key, value, ttl):
        self._reconnect_if_needed()
        if not self.conn:
            print("Redis unavailable. Cannot perform 'set'.")
            return
        try:
            self.conn.set(key, value, ttl)
            print(f"SET key='{key}' with TTL={ttl}s")
        except RedisError as e:
            print(f"Redis SET failed: {e}")
            self.conn = None

    def exists(self, key):
        """
        Check if key exists in Redis.
        """
        self._reconnect_if_needed()
        if not self.conn:
            print("Redis unavailable. Cannot perform 'exists'.")
            return False
        try:
            return self.conn.exists(key) == 1
        except RedisError as e:
            print(f"Redis EXISTS failed: {e}")
            self.conn = None
            return False


    def get_key(self, key):
        """
        Get key value.
        """
        self._reconnect_if_needed()
        if not self.conn:
            print("Redis connection not available, skipping 'get'")
            return False
        try:
            return self.conn.get(key)
        except RedisError as e:
            print(f"Redis GET failed for key={key}: {e}")
            return False
        

if __name__ == '__main__':
    engine = RedisEngine(host='localhost', port = 6379)
    if engine.conn:
        try:
            engine.conn.ping()
            print("Connected to Redis successfully.")
        except redis.exceptions.RedisError as e:
            print(f"Ping failed: {e}")
    else:
        print("Connection to Redis failed.")