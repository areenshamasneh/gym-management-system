from django.shortcuts import get_object_or_404

from gym_app.models import HallMachine, Hall, Machine


class MachineRepository:
    @staticmethod
    def create_hall_machine(gym_id, hall_id, data):
        hall = get_object_or_404(Hall, pk=hall_id, gym_id=gym_id)
        machine = get_object_or_404(Machine, id=data.get("machine_id"))
        return HallMachine.objects.create(
            hall_id=hall, machine_id=machine, name=data.get("name"), uid=data.get("uid")
        )

    @staticmethod
    def get_all_machines_in_hall(gym_id, hall_id):
        return HallMachine.objects.filter(hall_id_id=hall_id, hall_id__gym_id=gym_id)

    @staticmethod
    def get_machine_by_id_in_hall(gym_id, hall_id, machine_id):
        return get_object_or_404(
            HallMachine, hall_id_id=hall_id, hall_id__gym_id=gym_id, machine_id=machine_id
        )

    def update_hall_machine(self, gym_id, hall_id, machine_id, data):
        hall_machine = self.get_machine_by_id_in_hall(gym_id, hall_id, machine_id)
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

    def delete_hall_machine(self, gym_id, hall_id, machine_id):
        hall_machine = self.get_machine_by_id_in_hall(gym_id, hall_id, machine_id)
        hall_machine.delete()
