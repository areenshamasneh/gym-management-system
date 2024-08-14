from gym_app.exceptions import ResourceNotFoundException, DatabaseException
from gym_app.logging import SimpleLogger
from gym_app.repositories.hall_type_repository import HallTypeRepository


class HallTypeComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else HallTypeRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("HallTypeComponent initialized")

    def fetch_all_hall_types(self):
        self.logger.log_info("Fetching all hall types")
        try:
            hall_types = self.repo.get_all_hall_types()
            if not hall_types:
                raise ResourceNotFoundException("No hall types available.")
            return hall_types
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise ResourceNotFoundException("Resource not found")
        except Exception as e:
            self.logger.log_error(f"Error fetching all hall types: {e}")
            raise DatabaseException("An error occurred while fetching all hall types.") from e

    def fetch_hall_type_by_id(self, hall_type_id):
        self.logger.log_info(f"Fetching hall type with ID {hall_type_id}")
        try:
            hall_type = self.repo.get_hall_type_by_id(hall_type_id)
            if hall_type is None:
                raise ResourceNotFoundException(f"Hall type with ID {hall_type_id} does not exist.")
            return hall_type
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise ResourceNotFoundException("Resource not found")
        except Exception as e:
            self.logger.log_error(f"Error fetching hall type with ID {hall_type_id}: {e}")
            raise DatabaseException("An error occurred while fetching the hall type.") from e

    def add_hall_type(self, data):
        self.logger.log_info(f"Adding new hall type with data: {data}")
        try:
            return self.repo.create_hall_type(data)
        except DatabaseException as e:
            self.logger.log_error(f"Error adding hall type: {e}")
            raise

    def modify_hall_type(self, hall_type_id, data):
        self.logger.log_info(f"Modifying hall type with ID {hall_type_id} with data: {data}")
        try:
            return self.repo.update_hall_type(hall_type_id, data)
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except DatabaseException as e:
            self.logger.log_error(f"Error modifying hall type with ID {hall_type_id}: {e}")
            raise

    def remove_hall_type(self, hall_type_id):
        self.logger.log_info(f"Removing hall type with ID {hall_type_id}")
        try:
            self.repo.delete_hall_type(hall_type_id)
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except DatabaseException as e:
            self.logger.log_error(f"Error removing hall type with ID {hall_type_id}: {e}")
            raise
