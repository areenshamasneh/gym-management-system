from gym_app.repositories.gym_repository import GymRepository
from gym_app.logging import CustomLogger
from gym_app.models import Gym


class GymComponent:
    def __init__(self, gym_repository: GymRepository, logger: CustomLogger):
        self.gym_repository = gym_repository
        self.logger = logger
        self._initiate_component()

    def _initiate_component(self):
        self.logger.log_info("GymComponent initialized")

    def fetch_all_gyms(self):
        try:
            self.logger.log_info("Fetching all gyms")
            gyms = self.gym_repository.get_all_gyms()
            return gyms
        except Exception as e:
            self.logger.log_error(f"Error fetching gyms: {str(e)}")
            raise

    def fetch_gym_by_id(self, pk):
        try:
            self.logger.log_info(f"Fetching gym by ID {pk}")
            gym = self.gym_repository.get_gym_by_id(pk)
            return gym
        except Gym.DoesNotExist:
            self.logger.log_error(f"Gym with ID {pk} not found")
            raise
        except Exception as e:
            self.logger.log_error(f"Error fetching gym by ID {pk}: {str(e)}")
            raise

    def add_gym(self, data):
        try:
            self.logger.log_info("Adding new gym")
            gym = self.gym_repository.create_gym(data)
            return gym
        except Exception as e:
            self.logger.log_error(f"Error adding gym: {str(e)}")
            raise

    def modify_gym(self, pk, data):
        try:
            self.logger.log_info(f"Modifying gym ID {pk}")
            gym = self.gym_repository.update_gym(pk, data)
            return gym
        except Gym.DoesNotExist:
            self.logger.log_error(f"Gym with ID {pk} not found")
            raise
        except Exception as e:
            self.logger.log_error(f"Error modifying gym ID {pk}: {str(e)}")
            raise

    def remove_gym(self, pk):
        try:
            self.logger.log_info(f"Removing gym ID {pk}")
            self.gym_repository.delete_gym(pk)
        except Gym.DoesNotExist:
            self.logger.log_error(f"Gym with ID {pk} not found")
            raise
        except Exception as e:
            self.logger.log_error(f"Error removing gym ID {pk}: {str(e)}")
            raise
