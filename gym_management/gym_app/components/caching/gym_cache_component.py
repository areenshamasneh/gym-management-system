import json

from common.redis.cache_manager import CacheManager
from common.redis.redis import redis_client
from gym_app.serializers.v1.serializers import GymSchema


class GymCacheComponent:
    def __init__(self):
        self.cache_manager = CacheManager(prefix="gyms", redis_client=redis_client)
        self.gym_schema = GymSchema()
        self.version_key = "gyms_cache_version"

    def get_version(self):
        version = self.cache_manager.get(self.version_key)
        if not version:
            version = 1
            self.cache_manager.set(self.version_key, version)
        return version

    def increment_version(self):
        version = self.get_version()
        new_version = int(version) + 1
        self.cache_manager.set(self.version_key, new_version)

    def get_all_items(self, page_number, page_size, cache_version):
        cached_key = f"gyms_page_{cache_version}_{page_number}_size_{page_size}"
        cached_data = self.cache_manager.get(cached_key)

        if cached_data:
            try:
                cached_response = json.loads(cached_data)
                if isinstance(cached_response,
                              dict) and 'items' in cached_response and 'total_items' in cached_response:
                    return cached_response
            except json.JSONDecodeError:
                return {}

        return {}

    def cache_all_items(self, gyms, total_gyms, page_number, page_size, cache_version):
        cached_key = f"gyms_page_{cache_version}_{page_number}_size_{page_size}"
        serialized_gyms = [self.gym_schema.serialize_gym(gym) for gym in gyms]

        cached_data = json.dumps({
            'items': serialized_gyms,
            'total_items': total_gyms,
            'total_pages': (total_gyms + page_size - 1) // page_size,
            'current_page': page_number,
            'page_size': page_size,
        })

        self.cache_manager.set(cached_key, cached_data)

    def get_item(self, gym_id):
        cached_key = f"gym_{gym_id}"
        cached_data = self.cache_manager.get(cached_key)
        if cached_data:
            return json.loads(cached_data)
        return None

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
