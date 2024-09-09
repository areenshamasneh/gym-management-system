from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories.hall_machine_repository import HallMachineRepository


class HallMachineComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else HallMachineRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("HallMachineComponent initialized")

    def fetch_hall_machines_by_gym(self, gym_id):
        self.logger.log_info(f"Fetching hall machines for gym ID {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        hall_machine = self.repo.get_hall_machines_by_gym(gym)
        if not hall_machine:
            raise ResourceNotFoundException("No Hall Machines found for this gym")
        return hall_machine
