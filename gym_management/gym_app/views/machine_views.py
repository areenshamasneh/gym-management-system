from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
from gym_app.components.machine_component import (
    get_all_machines,
    get_machine_by_id,
    create_machine,
    update_machine,
    delete_machine,
)

@method_decorator(csrf_exempt, name="dispatch")
class MachineListView(View):
    def get(self, request):
        machines = get_all_machines()
        data = [
            {
                "serial_number": machine.serial_number,
                "type": machine.type,
                "model": machine.model,
                "brand": machine.brand,
                "status": machine.status,
                "maintenance_date": machine.maintenance_date,
            }
            for machine in machines
        ]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class MachineDetailView(View):
    def get(self, request, pk):
        machine = get_machine_by_id(pk)
        machine_data = {
            "serial_number": machine.serial_number,
            "type": machine.type,
            "model": machine.model,
            "brand": machine.brand,
            "status": machine.status,
            "maintenance_date": machine.maintenance_date,
        }
        return JsonResponse(machine_data)


@method_decorator(csrf_exempt, name="dispatch")
class MachineCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        machine = create_machine(data)
        response_data = {
            "serial_number": machine.serial_number,
            "type": machine.type,
            "model": machine.model,
            "brand": machine.brand,
            "status": machine.status,
            "maintenance_date": machine.maintenance_date,
        }
        return JsonResponse(response_data, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class MachineUpdateView(View):
    def put(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)
        machine = update_machine(pk, data)
        response_data = {
            "serial_number": machine.serial_number,
            "type": machine.type,
            "model": machine.model,
            "brand": machine.brand,
            "status": machine.status,
            "maintenance_date": machine.maintenance_date,
        }
        return JsonResponse(response_data, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class MachineDeleteView(View):
    def delete(self, request, pk, *args, **kwargs):
        delete_machine(pk)
        return JsonResponse({"message": "Machine deleted"}, status=204)
