from gym_app.repositories.machine_repository import MachineRepository


class MachineComponent:
    @staticmethod
    def fetch_all_machines():
        return MachineRepository.get_all_machines()

    @staticmethod
    def fetch_machine_by_id(pk):
        return MachineRepository.get_machine_by_id(pk)

    @staticmethod
    def add_machine(data):
        return MachineRepository.create_machine(data)

    @staticmethod
    def modify_machine(pk, data):
        return MachineRepository.update_machine(pk, data)

    @staticmethod
    def remove_machine(pk):
        MachineRepository.delete_machine(pk)
