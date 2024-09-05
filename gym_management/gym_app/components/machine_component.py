from common.db.database import Session
from gym_app.logging import SimpleLogger
from gym_app.repositories import MachineRepository


class MachineComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo or MachineRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("MachineComponent initialized")

    def fetch_all_machines_in_gym(self, gym_id):
        self.logger.log_info(f"Fetching all machines for gym_id: {gym_id}")
        return self.repo.get_all_machines_in_gym(gym_id)

    def fetch_machine_by_id_in_gym(self, gym_id, machine_id):
        self.logger.log_info(f"Fetching machine with ID: {machine_id} for gym_id: {gym_id}")
        hall_machine = self.repo.get_machine_by_id_in_gym(gym_id, machine_id)
        return hall_machine.machine

    def fetch_all_machines_in_hall(self, gym_id, hall_id):
        self.logger.log_info(f"Fetching all machines for gym_id: {gym_id}, hall_id: {hall_id}")
        return self.repo.get_all_machines_in_hall(gym_id, hall_id)

    def fetch_machine_by_id_in_hall(self, gym_id, hall_id, machine_id):
        self.logger.log_info(f"Fetching machine by ID: {machine_id} in hall: {hall_id}")
        hall_machine = self.repo.get_machine_by_id_in_hall(gym_id, hall_id, machine_id)
        return hall_machine.machine

    def add_machine_and_hall_machine(self, gym_id, hall_id, machine_data):
        session = Session()
        self.logger.log_info(f"Adding machine with data: {machine_data}")
        machine = self.repo.create_machine(gym_id, machine_data)
        session.commit()
        self.repo.create_hall_machine(
            gym_id,
            hall_id,
            machine.id,
        )
        session.commit()
        return machine

    def modify_machine_and_hall_machine(self, gym_id, hall_id, machine_id, data):
        session = Session()
        self.logger.log_info(f"Modifying hall machine with ID: {machine_id} and data: {data}")
        hall_machine = self.repo.update_machine(gym_id, hall_id, machine_id, data)
        session.commit()

        hall_machine = self.repo.update_hall_machine(hall_machine, hall_machine.machine)
        session.commit()

        return hall_machine

    def remove_hall_machine(self, gym_id, hall_id, machine_id):
        session = Session()
        self.logger.log_info(f"Removing hall machine with ID: {machine_id}")
        success = self.repo.delete_hall_machine(gym_id, hall_id, machine_id)

        if success:
            session.commit()
            return success
        return False
