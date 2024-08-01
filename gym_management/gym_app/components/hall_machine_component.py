from gym_app.repositories.hall_machine_repository import HallMachineRepository
from gym_app.logging import SimpleLogger


class HallMachineComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else HallMachineRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("HallMachineComponent initialized")

    def fetch_hall_machines_by_gym(self, gym_id):
        self.logger.log_info(f"Fetching hall machines for gym ID {gym_id}")
        try:
            return self.repo.get_hall_machines_by_gym(gym_id)
        except ValueError as e:
            self.logger.log_error(f"Error fetching hall machines: {e}")
            raise e

    def fetch_hall_machines_by_hall(self, hall_id):
        self.logger.log_info(f"Fetching hall machines for hall ID {hall_id}")
        return self.repo.get_hall_machines_by_hall(hall_id)
