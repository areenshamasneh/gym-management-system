from gym_app.repositories.hall_machine_repository import HallMachineRepository


class HallMachineComponents:
    def __init__(self):
        self.repo = HallMachineRepository()

    def fetch_all_hall_machines(self, gym_id, hall_id=None):
        return self.repo.get_all_hall_machines(gym_id, hall_id=hall_id)

    def fetch_hall_machine_by_id(self, gym_id, hall_id, machine_id):
        return self.repo.get_hall_machine_by_id(gym_id, hall_id, machine_id)

    def add_hall_machine(self, gym_id, hall_id, data):
        return self.repo.create_hall_machine(gym_id, hall_id, data)

    def modify_hall_machine(self, gym_id, hall_id, machine_id, data):
        return self.repo.update_hall_machine(gym_id, hall_id, machine_id, data)

    def remove_hall_machine(self, gym_id, hall_id, machine_id):
        self.repo.delete_hall_machine(gym_id, hall_id, machine_id)
