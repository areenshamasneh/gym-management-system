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

    def fetch_all_machines_in_gym(self, gym_id):
        self.logger.log_info(f"Fetching all hall machines for gym_id: {gym_id}")
        try:
            return self.repo.get_all_hall_machines_in_gym(gym_id)
        except Exception as e:
            self.logger.log_error(f"Error fetching machines in gym: {e}")
            raise DatabaseException(
                "An error occurred while fetching machines in the gym."
            )

    def fetch_all_machines_in_hall(self, gym_id, hall_id):
        self.logger.log_info(
            f"Fetching all machines for gym_id: {gym_id}, hall_id: {hall_id}"
        )
        try:
            return self.repo.get_all_machines_in_hall(gym_id, hall_id)
        except Exception as e:
            self.logger.log_error(f"Error fetching machines in hall: {e}")
            raise DatabaseException(
                "An error occurred while fetching machines in the hall."
            )

    def fetch_machine_by_id_in_hall(self, gym_id, hall_id, machine_id):
        self.logger.log_info(f"Fetching machine by ID: {machine_id} in hall: {hall_id}")
        try:
            hall_machine = self.repo.get_machine_by_id_in_hall(
                gym_id, hall_id, machine_id
            )
            if not hall_machine:
                raise ResourceNotFoundException(
                    f"Machine with ID {machine_id} not found."
                )
            return hall_machine.machine_id
        except ResourceNotFoundException:
            self.logger.log_error(
                f"Machine with ID {machine_id} not found in hall: {hall_id}"
            )
            raise
        except Exception as e:
            self.logger.log_error(f"Error fetching machine by ID: {e}")
            raise DatabaseException(
                "An error occurred while fetching the machine by ID."
            )

    def add_hall_machine(self, gym_id, hall_id, data):
        self.logger.log_info(f"Adding hall machine with data: {data}")
        try:
            hall_machine = self.repo.create_hall_machine(gym_id, hall_id, data)
            self.logger.log_info(f"Added hall machine: {hall_machine}")
            return hall_machine
        except ValueError as e:
            self.logger.log_error(f"Error adding hall machine: {e}")
            raise ValidationException(f"Validation error: {str(e)}")
        except Exception as e:
            self.logger.log_error(f"Error adding hall machine: {e}")
            raise DatabaseException("An error occurred while adding the hall machine.")

    def modify_hall_machine(self, gym_id, hall_id, machine_id, data):
        self.logger.log_info(
            f"Modifying hall machine with ID: {machine_id} and data: {data}"
        )
        try:
            hall_machine = self.repo.update_hall_machine(
                gym_id, hall_id, machine_id, data
            )
            if not hall_machine:
                raise ResourceNotFoundException(
                    f"Machine with ID {machine_id} not found."
                )
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
            raise DatabaseException(
                "An error occurred while modifying the hall machine."
            )

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
            raise DatabaseException(
                "An error occurred while removing the hall machine."
            )
