import json
from common.redis.cache_manager import CacheManager
from common.redis.redis import redis_client
from gym_app.components.caching.cache_component import CacheComponent
from gym_app.serializers.v1.serializers import GymSchema

class GymCacheComponent:
    def __init__(self):
        self.cache_component = CacheComponent(prefix="gyms", cache_manager=CacheManager(prefix="gyms", redis_client=redis_client))
        self.gym_schema = GymSchema()

    def get_item(self, gym_id):
        cached_data = self.cache_component.get_item(f"gym_{gym_id}")
        if cached_data:
            return json.loads(cached_data)
        return None

    def cache_item(self, gym_id, gym):
        serialized_gym = self.gym_schema.dump(gym)
        cached_data = json.dumps(serialized_gym)
        self.cache_component.cache_item(f"gym_{gym_id}", cached_data)

    def delete_item_cache(self, gym_id):
        self.cache_component.delete_item_cache(f"gym_{gym_id}")

    def clear_all_cache(self):
        self.cache_component.delete_all_items_cache()
