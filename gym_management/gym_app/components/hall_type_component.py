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
            return self.repo.get_all_hall_types()
        except Exception as e:
            self.logger.log_error(f"Error fetching all hall types: {e}")
            raise DatabaseException(
                "An error occurred while fetching all hall types."
            ) from e

    def fetch_hall_type_by_id(self, hall_type_id):
        self.logger.log_info(f"Fetching hall type with ID {hall_type_id}")
        try:
            hall_type = self.repo.get_hall_type_by_id(hall_type_id)
            if not hall_type:
                raise ResourceNotFoundException(
                    f"Hall type with ID {hall_type_id} not found."
                )
            return hall_type
        except ResourceNotFoundException:
            self.logger.log_error(f"Hall type with ID {hall_type_id} not found.")
            raise
        except Exception as e:
            self.logger.log_error(
                f"Error fetching hall type with ID {hall_type_id}: {e}"
            )
            raise DatabaseException(
                "An error occurred while fetching the hall type."
            ) from e

    def add_hall_type(self, data):
        self.logger.log_info(f"Adding new hall type with data: {data}")
        try:
            return self.repo.create_hall_type(data)
        except Exception as e:
            self.logger.log_error(f"Error adding hall type: {e}")
            raise DatabaseException(
                "An error occurred while adding the hall type."
            ) from e

    def modify_hall_type(self, hall_type_id, data):
        self.logger.log_info(
            f"Modifying hall type with ID {hall_type_id} with data: {data}"
        )
        try:
            updated_hall_type = self.repo.update_hall_type(hall_type_id, data)
            if not updated_hall_type:
                raise ResourceNotFoundException(
                    f"Hall type with ID {hall_type_id} not found."
                )
            return updated_hall_type
        except ResourceNotFoundException:
            self.logger.log_error(f"Hall type with ID {hall_type_id} not found.")
            raise
        except Exception as e:
            self.logger.log_error(
                f"Error modifying hall type with ID {hall_type_id}: {e}"
            )
            raise DatabaseException(
                "An error occurred while modifying the hall type."
            ) from e

    def remove_hall_type(self, hall_type_id):
        self.logger.log_info(f"Removing hall type with ID {hall_type_id}")
        try:
            if not self.repo.delete_hall_type(hall_type_id):
                raise ResourceNotFoundException(
                    f"Hall type with ID {hall_type_id} not found."
                )
        except ResourceNotFoundException:
            self.logger.log_error(f"Hall type with ID {hall_type_id} not found.")
            raise
        except Exception as e:
            self.logger.log_error(
                f"Error removing hall type with ID {hall_type_id}: {e}"
            )
            raise DatabaseException(
                "An error occurred while removing the hall type."
            ) from e
