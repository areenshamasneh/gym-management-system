from gym_app.models import Machine
from django.shortcuts import get_object_or_404


class MachineRepository:
    @staticmethod
    def get_all_machines():
        return Machine.objects.all()

    @staticmethod
    def get_machine_by_id(pk):
        return get_object_or_404(Machine, pk=pk)

    @staticmethod
    def create_machine(data):
        return Machine.objects.create(
            serial_number=data.get("serial_number"),
            type=data.get("type"),
            model=data.get("model"),
            brand=data.get("brand"),
            status=data.get("status"),
            maintenance_date=data.get("maintenance_date"),
        )

    @staticmethod
    def update_machine(pk, data):
        machine = get_object_or_404(Machine, pk=pk)
        machine.serial_number = data.get("serial_number", machine.serial_number)
        machine.type = data.get("type", machine.type)
        machine.model = data.get("model", machine.model)
        machine.brand = data.get("brand", machine.brand)
        machine.status = data.get("status", machine.status)
        machine.maintenance_date = data.get(
            "maintenance_date", machine.maintenance_date
        )
        machine.save()
        return machine

    @staticmethod
    def delete_machine(pk):
        machine = get_object_or_404(Machine, pk=pk)
        machine.delete()
