import json
from common.redis.cache_manager import CacheManager
from common.redis.redis import redis_client
from gym_app.serializers.v1.serializers import GymSchema


class GymCacheComponent:
    def __init__(self):
        self.cache_manager = CacheManager(prefix="gyms", redis_client=redis_client)
        self.gym_schema = GymSchema()

    def get_all_items(self, page_number, page_size):
        cached_key = f"gyms_page_{page_number}_size_{page_size}"
        cached_data = self.cache_manager.get(cached_key)
        if cached_data:
            return json.loads(cached_data)
        return []

    def get_item(self, gym_id):
        cached_key = f"gym_{gym_id}"
        cached_data = self.cache_manager.get(cached_key)
        if cached_data:
            return json.loads(cached_data)
        return None

    def cache_all_items(self, gyms, page_number, page_size):
        serialized_gyms = self.gym_schema.dump(gyms, many=True)
        cached_key = f"gyms_page_{page_number}_size_{page_size}"
        cached_data = json.dumps(serialized_gyms)
        self.cache_manager.set(cached_key, cached_data)

    def cache_item(self, gym_id, gym):
        serialized_gym = self.gym_schema.dump(gym)
        cached_key = f"gym_{gym_id}"
        cached_data = json.dumps(serialized_gym)
        self.cache_manager.set(cached_key, cached_data)

    def delete_item_cache(self, gym_id):
        cached_key = f"gym_{gym_id}"
        self.cache_manager.delete(cached_key)

    def clear_all_cache(self):
        self.cache_manager.clear_all_cache()
