from django.shortcuts import get_object_or_404

from gym_app.models import HallMachine, Hall, Machine


class MachineRepository:

    @staticmethod
    def get_all_machines_in_hall(gym_id, hall_id):
        return HallMachine.objects.filter(hall__id=hall_id, hall__gym_id=gym_id)

    @staticmethod
    def get_machine_by_id_in_hall(gym_id, hall_id, machine_id):
        return HallMachine.objects.filter(hall__id=hall_id, hall__gym_id=gym_id, machine__id=machine_id).first()

    @staticmethod
    def create_hall_machine(gym_id, hall_id, data):
        hall = get_object_or_404(Hall, pk=hall_id, gym_id=gym_id)
        machine = get_object_or_404(Machine, id=data.get("machine_id"))
        return HallMachine.objects.create(
            hall=hall,
            machine=machine,
            name=data.get("name"),
            uid=data.get("uid")
        )

    @staticmethod
    def update_hall_machine(gym_id, hall_id, machine_id, data):
        hall_machine = MachineRepository.get_machine_by_id_in_hall(gym_id, hall_id, machine_id)
        if "hall_id" in data:
            hall_instance = get_object_or_404(Hall, pk=data.get("hall_id"), gym_id=gym_id)
            hall_machine.hall = hall_instance
        if "machine_id" in data:
            machine_instance = get_object_or_404(Machine, id=data.get("machine_id"))
            hall_machine.machine = machine_instance
        if "name" in data:
            hall_machine.name = data.get("name")
        if "uid" in data:
            hall_machine.uid = data.get("uid")
        hall_machine.save()
        return hall_machine

    @staticmethod
    def delete_hall_machine(gym_id, hall_id, machine_id):
        hall_machine = MachineRepository.get_machine_by_id_in_hall(gym_id, hall_id, machine_id)
        hall_machine.delete()

    @staticmethod
    def get_all_machines_in_gym(gym_id):
        return HallMachine.objects.filter(hall__gym_id=gym_id)

    @staticmethod
    def get_machine_by_id_in_gym(gym_id, machine_id):
        return HallMachine.objects.filter(hall__gym_id=gym_id, machine__id=machine_id).first()
