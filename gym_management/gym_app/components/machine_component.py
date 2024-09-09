from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories import MachineRepository


class MachineComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo or MachineRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("MachineComponent initialized")

    def fetch_all_machines_in_gym(self, gym_id):
        self.logger.log_info(f"Fetching all machines for gym_id: {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        gym_machines = self.repo.get_all_machines_in_gym(gym)
        if not gym_machines:
            raise ResourceNotFoundException(f"No machines found in gym_id {gym_id}.")
        return gym_machines

    def fetch_machine_by_id_in_gym(self, gym_id, machine_id):
        self.logger.log_info(f"Fetching machine with ID: {machine_id} for gym_id: {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        hall_machine = self.repo.get_machine_by_id_in_gym(gym, machine_id)
        if not hall_machine:
            raise ResourceNotFoundException(f"Machine with ID {machine_id} not found in gym_id {gym_id}.")
        return hall_machine.machine

    def fetch_all_machines_in_hall(self, gym_id, hall_id):
        self.logger.log_info(f"Fetching all machines for gym_id: {gym_id}, hall_id: {hall_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        hall_machines = self.repo.get_all_machines_in_hall(gym, hall_id)
        if not hall_machines:
            raise ResourceNotFoundException(f"No machines found in hall_id {hall_id} for gym_id {gym_id}.")
        return hall_machines

    def fetch_machine_by_id_in_hall(self, gym_id, hall_id, machine_id):
        self.logger.log_info(f"Fetching machine by ID: {machine_id} in hall: {hall_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        hall_machine = self.repo.get_machine_by_id_in_hall(gym, hall_id, machine_id)
        if not hall_machine:
            raise ResourceNotFoundException(f"Machine with ID {machine_id} not found in hall_id {hall_id}.")
        return hall_machine.machine

    def add_machine_and_hall_machine(self, gym_id, hall_id, machine_data):
        self.logger.log_info(f"Adding machine with data: {machine_data}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        machine = self.repo.create_machine(machine_data)
        if not machine:
            raise ResourceNotFoundException("Failed to create machine")

        self.repo.create_hall_machine(hall_id, machine.id)
        Session.commit()
        return machine

    def modify_machine_and_hall_machine(self, gym_id, hall_id, machine_id, data):
        self.logger.log_info(f"Modifying hall machine with ID: {machine_id} and data: {data}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        hall_machine = self.repo.update_machine(gym, hall_id, machine_id, data)
        if not hall_machine:
            raise ResourceNotFoundException(f"Machine with ID {machine_id} not found in hall_id {hall_id}.")

        hall_machine = self.repo.update_hall_machine(hall_machine, hall_machine.machine)
        if not hall_machine:
            raise ResourceNotFoundException("Failed to update hall machine")

        Session.commit()
        return hall_machine

    def remove_hall_machine(self, gym_id, hall_id, machine_id):
        self.logger.log_info(f"Removing hall machine with ID: {machine_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        success = self.repo.delete_hall_machine(gym, hall_id, machine_id)
        if success:
            Session.commit()
            return success
        raise ResourceNotFoundException("Failed to delete hall machine")
