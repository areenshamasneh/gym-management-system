from gym_app.models import HallMachine, Hall, Machine
from django.shortcuts import get_object_or_404


class HallMachineRepository:
    def get_all_hall_machines(self, hall_id=None, machine_id=None):
        if hall_id:
            return HallMachine.objects.filter(hall_id=hall_id)
        if machine_id:
            return HallMachine.objects.filter(machine_id=machine_id)
        return HallMachine.objects.all()

    def get_hall_machine_by_id(self, hall_id, machine_id):
        return get_object_or_404(HallMachine, hall_id=hall_id, machine_id=machine_id)

    def create_hall_machine(self, data):
        hall = get_object_or_404(Hall, pk=data.get("hall"))
        machine = get_object_or_404(Machine, pk=data.get("machine"))
        return HallMachine.objects.create(
            hall=hall, machine=machine, name=data.get("name"), uid=data.get("uid")
        )

    def update_hall_machine(self, hall_id, machine_id, data):
        hall_machine = self.get_hall_machine_by_id(hall_id, machine_id)
        if "hall" in data:
            hall_instance = get_object_or_404(Hall, pk=data.get("hall"))
            hall_machine.hall = hall_instance

        if "machine" in data:
            machine_instance = get_object_or_404(Machine, pk=data.get("machine"))
            hall_machine.machine = machine_instance

        if "name" in data:
            hall_machine.name = data.get("name")

        if "uid" in data:
            hall_machine.uid = data.get("uid")

        hall_machine.save()
        return hall_machine

    def delete_hall_machine(self, hall_id, machine_id):
        hall_machine = self.get_hall_machine_by_id(hall_id, machine_id)
        hall_machine.delete()
