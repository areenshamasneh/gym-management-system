from gym_app.repositories.machine_repository import MachineRepository


class MachineComponent:

    def fetch_all_machines():
        return MachineRepository.get_all_machines()

    def fetch_machine_by_id(pk):
        return MachineRepository.get_machine_by_id(pk)

    def add_machine(data):
        return MachineRepository.create_machine(data)

    def modify_machine(pk, data):
        return MachineRepository.update_machine(pk, data)

    def remove_machine(pk):
        MachineRepository.delete_machine(pk)
