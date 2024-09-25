import json
from common.redis import redis_client

class CacheManager:
    def __init__(self, prefix, expiration=3600):
        self.prefix = prefix
        self.expiration = expiration

    def _generate_key(self, key):
        return f"{self.prefix}:{key}"

    def get(self, key):
        redis_key = self._generate_key(key)
        cached_value = redis_client.get(redis_key)
        if cached_value:
            return json.loads(cached_value)
        return None

    def set(self, key, value):
        redis_key = self._generate_key(key)
        redis_client.setex(redis_key, self.expiration, json.dumps(value))

    def delete(self, key):
        redis_key = self._generate_key(key)
        redis_client.delete(redis_key)
