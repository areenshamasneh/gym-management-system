from gym_app.exceptions import (
    InvalidInputException,
    ResourceNotFoundException,
    DatabaseException,
)
from gym_app.logging import SimpleLogger
from gym_app.repositories import GymRepository


class GymComponent:
    def __init__(self, gym_repository=None, logger=None):
        self.gym_repository = gym_repository or GymRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("GymComponent initialized")

    def fetch_all_gyms(self, page_number=1, page_size=10):
        try:
            return self.gym_repository.get_all_gyms(page_number, page_size)
        except Exception as e:
            self.logger.log_error(f"An error occurred while fetching all gyms: {e}")
            raise DatabaseException("An error occurred while fetching all gyms.")

    def fetch_gym_by_id(self, gym_id):
        try:
            gym = self.gym_repository.get_gym_by_id(gym_id)
            if gym is None:
                raise ResourceNotFoundException(f"Gym with ID {gym_id} does not exist")
            return gym
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise ResourceNotFoundException(f"Resource not found for gym_id: {gym_id}")
        except Exception as e:
            self.logger.log_error(
                f"An error occurred while fetching gym by ID {gym_id}: {e}"
            )
            raise DatabaseException(
                f"An error occurred while fetching gym by ID {gym_id}."
            )

    def add_gym(self, data):
        try:
            self.logger.log_info("Adding new gym")
        except KeyError as e:
            missing_field = str(e).strip("'")
            raise InvalidInputException(f"Missing required field: '{missing_field}'")
        except ValueError as e:
            self.logger.log_error(f"Invalid data: {e}")
            raise DatabaseException("An error occurred while adding the gym.")
        except Exception as e:
            self.logger.log_error(f"An error occurred while adding the gym: {e}")
            raise DatabaseException("An error occurred while adding the gym.")

    def modify_gym(self, gym_id, data):
        try:
            self.logger.log_info(f"Modifying gym ID {gym_id}")
            return self.gym_repository.update_gym(gym_id, data)
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except ValueError as e:
            self.logger.log_error(f"Invalid data: {e}")
            raise DatabaseException(
                f"An error occurred while modifying gym ID {gym_id}."
            )
        except Exception as e:
            self.logger.log_error(
                f"An error occurred while modifying gym ID {gym_id}: {e}"
            )
            raise DatabaseException(
                f"An error occurred while modifying gym ID {gym_id}."
            )

    def remove_gym(self, gym_id):
        try:
            self.logger.log_info(f"Removing gym ID {gym_id}")
            return self.gym_repository.delete_gym(gym_id)
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(
                f"An error occurred while removing gym ID {gym_id}: {e}"
            )
            raise DatabaseException(
                f"An error occurred while removing gym ID {gym_id}."
            )
