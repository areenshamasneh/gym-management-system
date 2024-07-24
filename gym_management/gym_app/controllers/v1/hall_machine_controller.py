import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import HallMachineComponents


class HallMachineController(View):
    def __init__(self, *args, **kwargs):
        self.components = HallMachineComponents()
        super().__init__(*args, **kwargs)

    @method_decorator(csrf_exempt, name="dispatch")
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, hall_id=None, machine_id=None):
        try:
            if hall_id and machine_id:
                hall_machine = self.components.fetch_hall_machine_by_id(
                    hall_id, machine_id
                )
                data = model_to_dict(hall_machine)
                return JsonResponse(data)
            elif hall_id:
                hall_machines = self.components.fetch_all_hall_machines(hall_id=hall_id)
                data = [model_to_dict(hall_machine) for hall_machine in hall_machines]
                return JsonResponse(data, safe=False)
            elif machine_id:
                machine_halls = self.components.fetch_all_hall_machines(
                    machine_id=machine_id
                )
                data = [model_to_dict(hall_machine) for hall_machine in machine_halls]
                return JsonResponse(data, safe=False)
            else:
                return JsonResponse(
                    {"error": "Hall ID or Machine ID required"}, status=400
                )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request, hall_id=None):
        if not hall_id:
            return JsonResponse({"error": "Hall ID required"}, status=400)
        try:
            data = json.loads(request.body)
            data["hall"] = hall_id
            hall_machine = self.components.add_hall_machine(data)
            response_data = model_to_dict(hall_machine)
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Creation failed: {str(e)}"}, status=500)

    def put(self, request, hall_id, machine_id):
        try:
            data = json.loads(request.body)
            hall_machine = self.components.modify_hall_machine(
                hall_id, machine_id, data
            )
            response_data = model_to_dict(hall_machine)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Update failed: {str(e)}"}, status=500)

    def delete(self, request, hall_id, machine_id):
        try:
            self.components.remove_hall_machine(hall_id, machine_id)
            return JsonResponse(
                {"message": "HallMachine deleted successfully"}, status=204
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
