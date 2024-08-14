from gym_app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    DatabaseException,
)
from gym_app.logging import SimpleLogger
from gym_app.models import Hall
from gym_app.repositories import HallRepository


class HallComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else HallRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("HallComponent initialized")

    def fetch_all_halls(self, gym_id):
        self.logger.log_info(f"Fetching all halls for gym ID {gym_id}")
        try:
            halls = self.repo.get_all_halls(gym_id)
            if not halls:
                raise ResourceNotFoundException(f"No halls found for gym ID {gym_id}.")
            return halls
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(f"Error fetching all halls: {str(e)}")
            raise DatabaseException("An error occurred while fetching halls.") from e

    def fetch_hall_by_id(self, gym_id, hall_id):
        self.logger.log_info(f"Fetching hall with ID {hall_id} for gym ID {gym_id}")
        try:
            hall = self.repo.get_hall_by_id(gym_id, hall_id)
            if hall is None:
                raise ResourceNotFoundException(f"No halls found for gym ID {gym_id}.")
            return hall
        except Hall.DoesNotExist:
            raise ResourceNotFoundException(f"Hall with ID {hall_id} does not exist in gym ID {gym_id}")
        except Exception as e:
            self.logger.log_error(f"Error fetching hall by ID {hall_id}: {str(e)}")
            raise DatabaseException(f"An error occurred while fetching hall with ID {hall_id}.") from e

    def add_hall(self, gym_id, data):
        self.logger.log_info(f"Adding new hall with data: {data} for gym ID {gym_id}")
        try:
            hall = self.repo.create_hall(gym_id, data)
            self.logger.log_info(f"Hall added: {hall}")
            return hall
        except ValueError as e:
            self.logger.log_error(f"Error adding hall: {e}")
            raise ValidationException(f"Validation error: {str(e)}")
        except Exception as e:
            self.logger.log_error(f"Error adding hall: {str(e)}")
            raise DatabaseException("An error occurred while adding the hall.")

    def modify_hall(self, gym_id, hall_id, data):
        self.logger.log_info(
            f"Modifying hall with ID {hall_id} with data: {data} for gym ID {gym_id}"
        )
        try:
            hall = self.repo.update_hall(gym_id, hall_id, data)
            if not hall:
                raise ResourceNotFoundException(f"Hall with ID {hall_id} not found.")
            self.logger.log_info(f"Hall modified: {hall}")
            return hall
        except ResourceNotFoundException:
            self.logger.log_error(f"Hall with ID {hall_id} not found")
            raise
        except ValueError as e:
            self.logger.log_error(f"Error modifying hall: {e}")
            raise ValidationException(f"Validation error: {str(e)}")
        except Exception as e:
            self.logger.log_error(f"Error modifying hall: {str(e)}")
            raise DatabaseException("An error occurred while modifying the hall.")

    def remove_hall(self, gym_id, hall_id):
        self.logger.log_info(f"Removing hall with ID {hall_id} for gym ID {gym_id}")
        try:
            success = self.repo.delete_hall(gym_id, hall_id)
            if not success:
                raise ResourceNotFoundException(f"Hall with ID {hall_id} not found.")
            self.logger.log_info(f"Hall with ID {hall_id} removed successfully.")
        except ResourceNotFoundException:
            self.logger.log_error(f"Hall with ID {hall_id} not found")
            raise
        except Exception as e:
            self.logger.log_error(f"Error removing hall: {str(e)}")
            raise DatabaseException("An error occurred while removing the hall.")
