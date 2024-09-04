from common.db.database import Session
from gym_app.exceptions import (
    InvalidInputException,
    ResourceNotFoundException,
    DatabaseException,
)
from gym_app.logging import SimpleLogger
from gym_app.repositories.gym_repository import GymRepository


class GymComponent:
    def __init__(self, gym_repository=None, logger=None):
        self.gym_repository = gym_repository or GymRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("GymComponent initialized")

    def fetch_all_gyms(self, page_number=1, page_size=10):
        self.logger.log_info(f"Fetching all Gyms")
        return self.gym_repository.get_all_gyms(page_number, page_size)

    def fetch_gym_by_id(self, gym_id):
        self.logger.log_info(f"Fetching gym with id: {gym_id}")
        return self.gym_repository.get_gym_by_id(gym_id)

    def add_gym(self, data):
        session = Session()
        try:
            self.logger.log_info("Adding new gym")
            gym = self.gym_repository.create_gym(data)
            session.commit()
            return gym
        finally:
            Session.remove()

    def modify_gym(self, gym_id, data):
        session = Session()
        try:
            self.logger.log_info(f"Modifying gym ID {gym_id}")
            gym = self.gym_repository.update_gym(gym_id, data)
            if gym:
                session.commit()
                return gym
            return None
        finally:
            Session.remove()

    def remove_gym(self, gym_id):
        session = Session()
        try:
            self.logger.log_info(f"Removing gym ID {gym_id}")
            success = self.gym_repository.delete_gym(gym_id)
            if success:
                session.commit()
                return success
            return False
        finally:
            Session.remove()
