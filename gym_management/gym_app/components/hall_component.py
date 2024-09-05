from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories import HallRepository


class HallComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else HallRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("HallComponent initialized")

    def fetch_all_halls(self, gym_id):
        self.logger.log_info(f"Fetching all halls for gym ID {gym_id}")
        return self.repo.get_all_halls(gym_id)

    def fetch_hall_by_id(self, gym_id, hall_id):
        self.logger.log_info(f"Fetching hall with ID {hall_id} for gym ID {gym_id}")
        return self.repo.get_hall_by_id(gym_id, hall_id)

    def add_hall(self, gym_id, data):
        self.logger.log_info(f"Adding new hall with data: {data} for gym ID {gym_id}")
        session = Session()
        hall = self.repo.create_hall(gym_id, data)
        session.commit()
        return hall

    def modify_hall(self, gym_id, hall_id, data):
        self.logger.log_info(
            f"Modifying hall with ID {hall_id} with data: {data} for gym ID {gym_id}"
        )
        session = Session()
        hall = self.repo.update_hall(gym_id, hall_id, data)
        if not hall:
            raise ResourceNotFoundException(f"Hall with ID {hall_id} not found.")
        session.commit()
        return hall

    def remove_hall(self, gym_id, hall_id):
        self.logger.log_info(f"Removing hall with ID {hall_id} for gym ID {gym_id}")
        session = Session()
        success = self.repo.delete_hall(gym_id, hall_id)
        if not success:
            raise ResourceNotFoundException(f"Hall with ID {hall_id} not found.")
        session.commit()
        return success
