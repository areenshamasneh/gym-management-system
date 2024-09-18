from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories.gym_repository import GymRepository
from services.aws_services.service import ServiceFactory


class GymComponent:
    def __init__(self, gym_repository=None, logger=None):
        self.gym_repository = gym_repository or GymRepository()
        self.logger = logger or SimpleLogger()
        self.message_service = ServiceFactory.get_msg_service()
        self.logger.log_info("GymComponent initialized")

    def fetch_all_gyms(self, page_number=1, page_size=10):
        self.logger.log_info("Fetching all gyms")
        return self.gym_repository.get_all_gyms(page_number, page_size)

    def fetch_gym_by_id(self, gym_id):
        self.logger.log_info(f"Fetching gym with ID: {gym_id}")
        gym = self.gym_repository.get_gym_by_id(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        return gym

    def add_gym(self, data):
        self.logger.log_info("Adding new gym")
        gym = self.gym_repository.create_gym(data)
        Session.commit()
        self.message_service.publish_event('entity_added', {'gym_id': gym.id, 'data': data})
        return gym

    def modify_gym(self, gym_id, data):
        self.logger.log_info(f"Modifying gym with ID: {gym_id}")
        gym = self.gym_repository.update_gym(gym_id, data)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        Session.commit()
        self.message_service.publish_event('entity_updated', {'gym_id': gym.id, 'data': data})
        return gym

    def remove_gym(self, gym_id):
        self.logger.log_info(f"Removing gym with ID: {gym_id}")
        success = self.gym_repository.delete_gym(gym_id)
        if not success:
            raise ResourceNotFoundException("Gym not found")
        Session.commit()
        return success

