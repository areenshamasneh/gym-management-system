from gym_app.logging import CustomLogger
from gym_app.repositories.hall_machine_repository import (
    HallMachineRepository,
)  # Import your custom logger


class HallMachineComponents:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else HallMachineRepository()
        self.logger = logger if logger else CustomLogger()

    def fetch_all_hall_machines(self, gym_id, hall_id=None):
        self.logger.log(
            f"Fetching all hall machines for gym_id: {gym_id}, hall_id: {hall_id}"
        )
        return self.repo.get_all_hall_machines(gym_id, hall_id=hall_id)

    def fetch_hall_machine_by_id(self, gym_id, hall_id, machine_id):
        self.logger.log(f"Fetching hall machine by ID: {machine_id}")
        return self.repo.get_hall_machine_by_id(gym_id, hall_id, machine_id)

    def add_hall_machine(self, gym_id, hall_id, data):
        self.logger.log(f"Adding hall machine with data: {data}")
        try:
            hall_machine = self.repo.create_hall_machine(gym_id, hall_id, data)
            self.logger.log(f"Added hall machine: {hall_machine}")
            return hall_machine
        except ValueError as e:
            self.logger.log(f"Error adding hall machine: {e}")
            raise

    def modify_hall_machine(self, gym_id, hall_id, machine_id, data):
        self.logger.log(
            f"Modifying hall machine with ID: {machine_id} and data: {data}"
        )
        try:
            hall_machine = self.repo.update_hall_machine(
                gym_id, hall_id, machine_id, data
            )
            self.logger.log(f"Modified hall machine: {hall_machine}")
            return hall_machine
        except ValueError as e:
            self.logger.log(f"Error modifying hall machine: {e}")
            raise

    def remove_hall_machine(self, gym_id, hall_id, machine_id):
        self.logger.log(f"Removing hall machine with ID: {machine_id}")
        try:
            self.repo.delete_hall_machine(gym_id, hall_id, machine_id)
            self.logger.log(f"Removed hall machine with ID: {machine_id}")
        except ValueError as e:
            self.logger.log(f"Error removing hall machine: {e}")
            raise
