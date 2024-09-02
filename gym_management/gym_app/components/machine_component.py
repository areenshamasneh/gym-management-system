from gym_app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    DatabaseException,
)
from gym_app.logging import SimpleLogger
from gym_app.repositories import MachineRepository


class MachineComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else MachineRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("MachineComponent initialized")

    def fetch_all_machines_in_hall(self, gym_id, hall_id):
        self.logger.log_info(f"Fetching all machines for gym_id: {gym_id}, hall_id: {hall_id}")
        try:
            halls_machines = self.repo.get_all_machines_in_hall(gym_id, hall_id)
            if not halls_machines:
                raise ResourceNotFoundException(f"There are no machines in hall {hall_id} for gym_id {gym_id}.")
            return halls_machines
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(f"Error fetching machines in hall: {e}")
            raise DatabaseException("An error occurred while fetching machines in the hall.") from e

    def fetch_machine_by_id_in_hall(self, gym_id, hall_id, machine_id):
        self.logger.log_info(f"Fetching machine by ID: {machine_id} in hall: {hall_id}")
        try:
            hall_machine = self.repo.get_machine_by_id_in_hall(gym_id, hall_id, machine_id)
            if not hall_machine:
                raise ResourceNotFoundException(
                    f"Machine with ID {machine_id} not found in hall: {hall_id} for gym_id {gym_id}.")
            return hall_machine.machine
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(f"Error fetching machine by ID: {e}")
            raise DatabaseException("An error occurred while fetching the machine by ID.") from e

    def add_machine_and_hall_machine(self, gym_id, hall_id, machine_data):
        self.logger.log_info(f"Adding machine with data: {machine_data}")
        try:
            machine = self.repo.create_machine(machine_data)
            self.repo.create_hall_machine(
                gym_id,
                hall_id,
                machine.id,
            )
            return machine
        except ValueError as e:
            self.logger.log_error(f"Error adding machine and hall machine: {e}")
            raise ValidationException(f"Validation error: {str(e)}")
        except Exception as e:
            self.logger.log_error(f"Error adding machine and hall machine: {e}")
            raise DatabaseException("An error occurred while adding the machine and hall machine.")

    def modify_machine_and_hall_machine(self, gym_id, hall_id, machine_id, data):
        self.logger.log_info(f"Modifying hall machine with ID: {machine_id} and data: {data}")
        try:
            hall_machine = self.repo.update_machine_and_hall_machine(gym_id, hall_id, machine_id, data)
            self.logger.log_info(f"Modified hall machine: {hall_machine}")
            return hall_machine
        except ResourceNotFoundException:
            self.logger.log_error(f"Machine with ID {machine_id} not found.")
            raise
        except ValueError as e:
            self.logger.log_error(f"Error modifying hall machine: {e}")
            raise ValidationException(f"Validation error: {str(e)}")
        except Exception as e:
            self.logger.log_error(f"Error modifying hall machine: {e}")
            raise DatabaseException("An error occurred while modifying the hall machine.")

    def remove_hall_machine(self, gym_id, hall_id, machine_id):
        self.logger.log_info(f"Removing hall machine with ID: {machine_id}")
        try:
            self.repo.delete_hall_machine(gym_id, hall_id, machine_id)
            self.logger.log_info(f"Removed hall machine with ID: {machine_id}")
        except ValueError as e:
            self.logger.log_error(f"Error removing hall machine: {e}")
            raise ValidationException(f"Validation error: {str(e)}")
        except Exception as e:
            self.logger.log_error(f"Error removing hall machine: {e}")
            raise DatabaseException("An error occurred while removing the hall machine.")

    def fetch_all_machines_in_gym(self, gym_id):
        self.logger.log_info(f"Fetching all machines for gym_id: {gym_id}")
        try:
            gym_machines = self.repo.get_all_machines_in_gym(gym_id)
            if not gym_machines:
                raise ResourceNotFoundException(f"There are no machines in gym_id {gym_id}.")
            return gym_machines
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(f"Error fetching machines in gym: {e}")
            raise DatabaseException("An error occurred while fetching machines in the gym.") from e

    def fetch_machine_by_id_in_gym(self, gym_id, machine_id):
        self.logger.log_info(f"Fetching machine with ID: {machine_id} for gym_id: {gym_id}")
        try:
            hall_machine = self.repo.get_machine_by_id_in_gym(gym_id, machine_id)
            if not hall_machine:
                raise ResourceNotFoundException(
                    f"Machine with ID {machine_id} not found in any hall for gym_id {gym_id}.")
            return hall_machine.machine
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(f"Error fetching machine by ID: {e}")
            raise DatabaseException("An error occurred while fetching the machine by ID.") from e
