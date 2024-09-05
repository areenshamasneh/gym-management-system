from common.db.database import Session
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
        hall_types = self.repo.get_all_hall_types()
        if not hall_types:
            self.logger.log_info("No hall types found")
            raise ResourceNotFoundException("No hall types found")
        return hall_types

    def fetch_hall_type_by_id(self, hall_type_id):
        self.logger.log_info(f"Fetching hall type with ID {hall_type_id}")
        hall_type = self.repo.get_hall_type_by_id(hall_type_id)
        if not hall_type:
            raise ResourceNotFoundException(f"HallType with ID {hall_type_id} not found")
        return hall_type

    def add_hall_type(self, data):
        self.logger.log_info(f"Adding new hall type with data: {data}")
        hall_type = self.repo.create_hall_type(data)
        if not hall_type:
            raise DatabaseException("Code already exists for another hall type.")
        Session.commit()
        return hall_type

    def modify_hall_type(self, hall_type_id, data):
        self.logger.log_info(f"Modifying hall type with ID {hall_type_id} with data: {data}")
        hall_type = self.repo.update_hall_type(hall_type_id, data)
        if not hall_type:
            raise ResourceNotFoundException(f"HallType with ID {hall_type_id} not found or code in use")
        Session.commit()
        return hall_type

    def remove_hall_type(self, hall_type_id):
        self.logger.log_info(f"Removing hall type with ID {hall_type_id}")
        success = self.repo.delete_hall_type(hall_type_id)
        if not success:
            raise ResourceNotFoundException(f"HallType with ID {hall_type_id} not found or still in use")
        Session.commit()
        return success
