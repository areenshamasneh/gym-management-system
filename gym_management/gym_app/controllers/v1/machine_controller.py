import json
from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gym_app.components.machine_component import MachineComponent
from gym_app.models import Machine


@method_decorator(csrf_exempt, name="dispatch")
class MachineController(View):
    def get(self, request, pk=None):
        if pk:
            try:
                machine = MachineComponent.fetch_machine_by_id(pk)
                machine_data = {
                    "serial_number": machine.serial_number,
                    "type": machine.type,
                    "model": machine.model,
                    "brand": machine.brand,
                    "status": machine.status,
                    "maintenance_date": machine.maintenance_date,
                }
                return JsonResponse(machine_data)
            except Http404:
                return JsonResponse({"error": "Machine not found"}, status=404)
        else:
            machines = MachineComponent.fetch_all_machines()
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

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            machine = MachineComponent.add_machine(data)
            response_data = {
                "serial_number": machine.serial_number,
                "type": machine.type,
                "model": machine.model,
                "brand": machine.brand,
                "status": machine.status,
                "maintenance_date": machine.maintenance_date,
            }
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Creation failed", "details": str(e)}, status=500
            )

    def put(self, request, pk, *args, **kwargs):
        try:
            data = json.loads(request.body)
            machine = MachineComponent.modify_machine(pk, data)
            response_data = {
                "serial_number": machine.serial_number,
                "type": machine.type,
                "model": machine.model,
                "brand": machine.brand,
                "status": machine.status,
                "maintenance_date": machine.maintenance_date,
            }
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Http404:
            return JsonResponse({"error": "Machine not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, pk, *args, **kwargs):
        try:
            MachineComponent.remove_machine(pk)
            return JsonResponse({"message": "Machine deleted"}, status=204)
        except Http404:
            return JsonResponse({"error": "Machine not found"}, status=404)
        except Exception as e:
            return JsonResponse(
                {"error": "Deletion failed", "details": str(e)}, status=500
            )
