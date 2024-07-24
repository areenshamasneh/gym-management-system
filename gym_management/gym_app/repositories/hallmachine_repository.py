from gym_app.models import HallMachine, Hall, Machine
from django.shortcuts import get_object_or_404


def get_all_hall_machines():
    return HallMachine.objects.all()


def get_hall_machine_by_id(hall_machine_id):
    return get_object_or_404(HallMachine, pk=hall_machine_id)


def create_hall_machine(data):
    hall_instance = get_object_or_404(Hall, pk=data.get("hall"))
    machine_instance = get_object_or_404(Machine, pk=data.get("machine"))

    return HallMachine.objects.create(
        hall=hall_instance,
        machine=machine_instance,
        name=data.get("name"),
        uid=data.get("uid"),
    )


def update_hall_machine(hall_machine_id, data):
    hall_machine = get_object_or_404(HallMachine, pk=hall_machine_id)

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


def delete_hall_machine(hall_machine_id):
    hall_machine = get_object_or_404(HallMachine, pk=hall_machine_id)
    hall_machine.delete()
