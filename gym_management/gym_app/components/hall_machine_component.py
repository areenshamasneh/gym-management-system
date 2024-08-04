from gym_app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    DatabaseException,
)
from gym_app.logging import SimpleLogger
from gym_app.repositories.hall_machine_repository import HallMachineRepository


class HallMachineComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else HallMachineRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("HallMachineComponent initialized")

    def fetch_hall_machines_by_gym(self, gym_id):
        self.logger.log_info(f"Fetching hall machines for gym ID {gym_id}")
        try:
            result = self.repo.get_hall_machines_by_gym(gym_id)
            if result is None:
                raise ResourceNotFoundException(
                    f"No hall machines found for gym ID {gym_id}."
                )
            return result
        except ValueError as e:
            self.logger.log_error(f"Error fetching hall machines: {e}")
            raise ValidationException(f"Validation error: {e}")
        except ResourceNotFoundException as e:
            self.logger.log_error(f"Error fetching hall machines: {e}")
            raise e
        except Exception as e:
            self.logger.log_error(f"Error fetching hall machines: {e}")
            raise DatabaseException("An error occurred while fetching hall machines.")

    def fetch_hall_machines_by_hall(self, hall_id):
        self.logger.log_info(f"Fetching hall machines for hall ID {hall_id}")
        try:
            result = self.repo.get_hall_machines_by_hall(hall_id)
            if result is None:
                raise ResourceNotFoundException(
                    f"No hall machines found for hall ID {hall_id}."
                )
            return result
        except ValueError as e:
            self.logger.log_error(f"Error fetching hall machines: {e}")
            raise ValidationException(f"Validation error: {e}")
        except ResourceNotFoundException as e:
            self.logger.log_error(f"Error fetching hall machines: {e}")
            raise e
        except Exception as e:
            self.logger.log_error(f"Error fetching hall machines: {e}")
            raise DatabaseException("An error occurred while fetching hall machines.")

    def fetch_hall_machine_by_id(self, machine_id):
        self.logger.log_info(f"Fetching hall machine with ID {machine_id}")
        try:
            result = self.repo.get_hall_machine_by_id(machine_id)
            if result is None:
                raise ResourceNotFoundException(
                    f"Hall machine with ID {machine_id} not found."
                )
            return result
        except ValueError as e:
            self.logger.log_error(f"Error fetching hall machine by ID: {e}")
            raise ValidationException(f"Validation error: {e}")
        except ResourceNotFoundException as e:
            self.logger.log_error(f"Error fetching hall machine by ID: {e}")
            raise e
        except Exception as e:
            self.logger.log_error(f"Error fetching hall machine by ID: {e}")
            raise DatabaseException(
                "An error occurred while fetching the hall machine."
            )
