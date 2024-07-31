from django.forms import model_to_dict
from django.http import Http404, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gym_app.components import HallMachineComponents
from gym_app.forms.hall_machine import HallMachineForm
from gym_app.models import Machine
import json


@method_decorator(csrf_exempt, name="dispatch")
class HallMachineController(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component = HallMachineComponents()

    def get(self, request, gym_id, hall_id=None, machine_id=None):
        try:
            if machine_id:
                # Fetch specific Machine associated with the hall
                machine = self.component.fetch_machine_by_id_in_hall(
                    gym_id, hall_id, machine_id
                )
                data = model_to_dict(machine)
                return JsonResponse(data)
            elif hall_id:
                # Fetch all Machines in the hall
                machines = self.component.fetch_all_machines_in_hall(gym_id, hall_id)
                data = [model_to_dict(machine) for machine in machines]
                return JsonResponse(data, safe=False)
            else:
                # Fetch all HallMachine records for the specified gym
                hall_machines = self.component.fetch_all_machines_in_gym(gym_id)
                data = [model_to_dict(hall_machine) for hall_machine in hall_machines]
                return JsonResponse(data, safe=False)
        except Http404:
            return JsonResponse({"error": "Machine or Hall not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request, gym_id, hall_id):
        data = json.loads(request.body)
        if "serial_number" not in data:
            return JsonResponse({"error": "serial_number is required"}, status=400)

        try:
            machine, created = Machine.objects.get_or_create(
                serial_number=data["serial_number"],
                defaults={
                    "type": data.get("type"),
                    "model": data.get("model"),
                    "brand": data.get("brand"),
                    "status": data.get("status"),
                    "maintenance_date": data.get("maintenance_date"),
                },
            )

            if created:
                self.component.logger.log_info(
                    f"Machine created: {machine.serial_number}"
                )
            else:
                self.component.logger.log_info(
                    f"Machine already exists: {machine.serial_number}"
                )

            hall_machine = self.component.add_hall_machine(
                gym_id,
                hall_id,
                {
                    "name": data.get("name"),
                    "uid": data.get("uid"),
                    "machine_id": machine.id,
                },
            )

            response_data = model_to_dict(hall_machine)
            return JsonResponse(response_data, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, gym_id, hall_id, machine_id):
        try:
            data = json.loads(request.body)
            form = HallMachineForm(data)
            if form.is_valid():
                hall_machine = self.component.modify_hall_machine(
                    gym_id, hall_id, machine_id, form.cleaned_data
                )
                response_data = model_to_dict(hall_machine)
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Http404:
            return JsonResponse({"error": "HallMachine not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, gym_id, hall_id, machine_id):
        try:
            self.component.remove_hall_machine(gym_id, hall_id, machine_id)
            return JsonResponse({"message": "Deleted successfully"}, status=204)
        except Http404:
            return JsonResponse({"error": "HallMachine not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
