
class CacheManager:
    def __init__(self, prefix, redis_client, expiration=3600):
        self.prefix = prefix
        self.redis_client = redis_client
        self.expiration = expiration

    def _generate_key(self, key):
        return f"{self.prefix}:{key}"

    def get(self, key):
        redis_key = self._generate_key(key)
        cached_value = self.redis_client.get(redis_key)
        if cached_value:
            return cached_value
        return None

    def set(self, key, value):
        redis_key = self._generate_key(key)
        self.redis_client.setex(redis_key, self.expiration, value)

    def delete(self, key):
        redis_key = self._generate_key(key)
        self.redis_client.delete(redis_key)

    def clear_all_cache(self):
        self.redis_client.flushdb()
