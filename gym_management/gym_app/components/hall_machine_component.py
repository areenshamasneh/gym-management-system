from gym_app.repositories import HallMachineRepository


class HallMachineComponents:
    def __init__(self):
        self.repo = HallMachineRepository()

    def fetch_all_hall_machines(self, hall_id=None, machine_id=None):
        return self.repo.get_all_hall_machines(hall_id=hall_id, machine_id=machine_id)

    def fetch_hall_machine_by_id(self, hall_id, machine_id):
        return self.repo.get_hall_machine_by_id(hall_id, machine_id)

    def add_hall_machine(self, data):
        return self.repo.create_hall_machine(data)

    def modify_hall_machine(self, hall_id, machine_id, data):
        return self.repo.update_hall_machine(hall_id, machine_id, data)

    def remove_hall_machine(self, hall_id, machine_id):
        self.repo.delete_hall_machine(hall_id, machine_id)
