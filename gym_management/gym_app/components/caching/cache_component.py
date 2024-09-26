from common.redis.cache_manager import CacheManager


class CacheComponent:
    def __init__(self, prefix, cache_manager=None):
        self.cache_manager = cache_manager or CacheManager(prefix=prefix)

    def get_item(self, item_id):
        return self.cache_manager.get(item_id)

    def cache_item(self, item_id, data):
        self.cache_manager.set(item_id, data)

    def delete_item_cache(self, item_id):
        self.cache_manager.delete(item_id)

    def get_all_items(self):
        return self.cache_manager.get_all()

    def cache_all_items(self, items_data):
        self.cache_manager.set_all(items_data)

    def delete_all_items_cache(self):
        self.cache_manager.delete_all()
