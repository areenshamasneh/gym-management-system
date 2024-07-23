from gym_app.models import Machine

def get_all_machines():
    return Machine.objects.all()

def get_machine_by_id(pk):
    return Machine.objects.get(pk=pk)

def create_machine(data):
    return Machine.objects.create(
        serial_number=data.get("serial_number"),
        type=data.get("type"),
        model=data.get("model"),
        brand=data.get("brand"),
        status=data.get("status"),
        maintenance_date=data.get("maintenance_date"),
    )

def update_machine(pk, data):
    machine = Machine.objects.get(pk=pk)
    machine.serial_number = data.get("serial_number", machine.serial_number)
    machine.type = data.get("type", machine.type)
    machine.model = data.get("model", machine.model)
    machine.brand = data.get("brand", machine.brand)
    machine.status = data.get("status", machine.status)
    machine.maintenance_date = data.get("maintenance_date", machine.maintenance_date)
    machine.save()
    return machine

def delete_machine(pk):
    Machine.objects.get(pk=pk).delete()
