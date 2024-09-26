from common.db.database import Session
from gym_app.components.caching import GymCacheComponent
from gym_app.components.sns import GymSNSComponent
from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories.gym_repository import GymRepository

class GymComponent:
    def __init__(self, gym_repository=None, logger=None, sns_component=None, cache_component=None):
        self.gym_repository = gym_repository or GymRepository()
        self.logger = logger or SimpleLogger()
        self.sns_component = sns_component or GymSNSComponent()
        self.cache_component = cache_component or GymCacheComponent()

    def fetch_all_gyms(self, page_number=1, page_size=10):
        self.logger.log_info("Fetching all gyms")
        cached_response = self.cache_component.get_all_items(page_number, page_size)

        if cached_response:
            return cached_response['items'], cached_response['total_items']

        gyms, total_gyms = self.gym_repository.get_all_gyms(page_number, page_size)
        if gyms:
            self.cache_component.cache_all_items(gyms, total_gyms, page_number, page_size)

        return gyms, total_gyms

    def fetch_gym_by_id(self, gym_id):
        self.logger.log_info(f"Fetching gym with ID: {gym_id}")
        cached_gym = self.cache_component.get_item(gym_id)
        if cached_gym:
            return cached_gym

        gym = self.gym_repository.get_gym_by_id(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        self.cache_component.cache_item(gym_id, gym)
        return gym

    def add_gym(self, data):
        self.logger.log_info("Adding new gym")
        gym = self.gym_repository.create_gym(data)
        Session.commit()
        self.sns_component.notify_gym_created(gym.id, data)
        self.cache_component.cache_item(gym.id, gym)
        self.cache_component.increment_version()
        return gym

    def modify_gym(self, gym_id, data):
        self.logger.log_info(f"Modifying gym with ID: {gym_id}")
        gym = self.gym_repository.update_gym(gym_id, data)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        Session.commit()
        self.cache_component.delete_item_cache(gym_id)
        self.cache_component.cache_item(gym_id, gym)
        self.sns_component.notify_gym_updated(gym.id, data)
        return gym

    def remove_gym(self, gym_id):
        self.logger.log_info(f"Removing gym with ID: {gym_id}")
        success = self.gym_repository.delete_gym(gym_id)
        if not success:
            raise ResourceNotFoundException("Gym not found")

        Session.commit()
        self.cache_component.delete_item_cache(gym_id)
        self.sns_component.notify_gym_deleted(gym_id)
        self.cache_component.increment_version()
        return success