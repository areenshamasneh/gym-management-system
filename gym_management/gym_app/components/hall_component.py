from gym_app.logging import SimpleLogger
from gym_app.repositories.hall_repository import HallRepository


class HallComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else HallRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("HallComponent initialized")

    def fetch_all_halls(self, gym_id):
        self.logger.log("Fetching all halls")
        return self.repo.get_all_halls(gym_id)

    def fetch_hall_by_id(self, gym_id, hall_id):
        self.logger.log_info(f"Fetching hall with ID {hall_id}")
        return self.repo.get_hall_by_id(gym_id, hall_id)

    def add_hall(self, gym_id, data):
        self.logger.log_info(f"Adding new hall with data: {data}")
        try:
            hall = self.repo.create_hall(gym_id, data)
            self.logger.log_info(f"Hall added: {hall}")
            return hall
        except ValueError as e:
            self.logger.log_error(f"Error adding hall: {e}")
            raise

    def modify_hall(self, gym_id, hall_id, data):
        self.logger.log_info(f"Modifying hall with ID {hall_id} with data: {data}")
        try:
            hall = self.repo.update_hall(gym_id, hall_id, data)
            self.logger.log_info(f"Hall modified: {hall}")
            return hall
        except ValueError as e:
            self.logger.log_error(f"Error modifying hall: {e}")
            raise

    def remove_hall(self, gym_id, hall_id):
        self.logger.log_info(f"Removing hall with ID {hall_id}")
        return self.repo.delete_hall(gym_id, hall_id)
