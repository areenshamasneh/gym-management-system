from common.db.database import Session
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

        return hall_types

    def fetch_hall_type_by_id(self, hall_type_id):
        self.logger.log_info(f"Fetching hall type with ID {hall_type_id}")
        hall_type = self.repo.get_hall_type_by_id(hall_type_id)

        return hall_type

    def add_hall_type(self, data):
        session = Session()
        self.logger.log_info(f"Adding new hall type with data: {data}")
        hall_type = self.repo.create_hall_type(data)
        session.commit()
        return hall_type

    def modify_hall_type(self, hall_type_id, data):
        session = Session()
        self.logger.log_info(f"Modifying hall type with ID {hall_type_id} with data: {data}")
        hall_type = self.repo.update_hall_type(hall_type_id, data)
        if hall_type:
            session.commit()
            return hall_type
        return None

    def remove_hall_type(self, hall_type_id):
        session = Session()
        self.logger.log_info(f"Removing hall type with ID {hall_type_id}")
        success = self.repo.delete_hall_type(hall_type_id)
        if success:
            session.commit()
            return success
        return False
