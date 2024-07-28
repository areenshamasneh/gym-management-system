from gym_app.logging import CustomLogger
from gym_app.repositories.hall_repository import HallRepository


class HallComponent:
    def __init__(self, repo: HallRepository, logger):
        self.repo = repo
        self.logger = logger

    def fetch_all_halls(self, gym_id):
        self.logger.log("Fetching all halls")
        return self.repo.get_all_halls(gym_id)

    def fetch_hall_by_id(self, gym_id, hall_id):
        self.logger.log(f"Fetching hall with ID {hall_id}")
        return self.repo.get_hall_by_id(gym_id, hall_id)

    def add_hall(self, gym_id, data):
        self.logger.log(f"Adding new hall with data: {data}")
        try:
            return self.repo.create_hall(gym_id, data)
        except ValueError as e:
            raise ValueError("Invalid data") from e

    def modify_hall(self, gym_id, hall_id, data):
        self.logger.log(f"Modifying hall with ID {hall_id} with data: {data}")
        return self.repo.update_hall(gym_id, hall_id, data)

    def remove_hall(self, gym_id, hall_id):
        self.logger.log(f"Removing hall with ID {hall_id}")
        return self.repo.delete_hall(gym_id, hall_id)
