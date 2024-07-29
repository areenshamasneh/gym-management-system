from gym_app.logging import SimpleLogger
from gym_app.repositories.hall_type_repository import HallTypeRepository


class HallTypeComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else HallTypeRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("HallTypeComponent initialized")

    def fetch_all_hall_types(self):
        self.logger.log("Fetching all hall types")
        return self.repo.get_all_hall_types()

    def fetch_hall_type_by_id(self, hall_type_id):
        self.logger.log(f"Fetching hall type with ID {hall_type_id}")
        return self.repo.get_hall_type_by_id(hall_type_id)

    def add_hall_type(self, data):
        self.logger.log(f"Adding new hall type with data: {data}")
        try:
            return self.repo.create_hall_type(data)
        except ValueError as e:
            self.logger.log(f"Error adding hall type: {e}")
            raise ValueError("Invalid data") from e

    def modify_hall_type(self, hall_type_id, data):
        self.logger.log(f"Modifying hall type with ID {hall_type_id} with data: {data}")
        return self.repo.update_hall_type(hall_type_id, data)

    def remove_hall_type(self, hall_type_id):
        self.logger.log(f"Removing hall type with ID {hall_type_id}")
        return self.repo.delete_hall_type(hall_type_id)
