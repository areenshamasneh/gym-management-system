from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories.hall_repository import HallRepository


class HallComponent:
    def __init__(self, hall_repository=None, logger=None):
        self.repo = hall_repository or HallRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("HallComponent initialized")

    def fetch_all_halls(self, gym_id):
        self.logger.log_info(f"Fetching all halls for gym ID {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        halls = self.repo.get_all_halls(gym)
        if not halls:
            raise ResourceNotFoundException("No halls found for this gym")

        return halls

    def fetch_hall_by_id(self, gym_id, hall_id):
        self.logger.log_info(f"Fetching hall with ID {hall_id} for gym ID {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        hall = self.repo.get_hall_by_id(gym, hall_id)
        if not hall:
            raise ResourceNotFoundException("Hall not found")

        return hall

    def add_hall(self, gym_id, data):
        self.logger.log_info(f"Adding new hall with data: {data} for gym ID {gym_id}")
        hall_type_id = data.get("hall_type")
        if hall_type_id is None:
            raise ValueError("HallType ID is required")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        hall = self.repo.create_hall(gym, data)
        Session.commit()
        return hall

    def modify_hall(self, gym_id, hall_id, data):
        self.logger.log_info(f"Modifying hall with ID {hall_id} with data: {data} for gym ID {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        hall = self.repo.update_hall(gym, hall_id, data)
        if not hall:
            raise ResourceNotFoundException("Hall not found")

        Session.commit()
        return hall

    def remove_hall(self, gym_id, hall_id):
        self.logger.log_info(f"Removing hall with ID {hall_id} for gym ID {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        success = self.repo.delete_hall(gym, hall_id)
        if not success:
            raise ResourceNotFoundException("Hall not found")

        Session.commit()
        return success
