import json
from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import HallMachineComponents


@method_decorator(csrf_exempt, name="dispatch")
class HallMachineController(View):
    def get(self, request, gym_id, hall_id, machine_id=None):
        if machine_id:
            try:
                hall_machine = HallMachineComponents().fetch_hall_machine_by_id(
                    gym_id, hall_id, machine_id
                )
                data = model_to_dict(hall_machine)
                return JsonResponse(data)
            except Http404:
                return JsonResponse({"error": "HallMachine not found"}, status=404)
        else:
            hall_machines = HallMachineComponents().fetch_all_hall_machines(
                gym_id, hall_id
            )
            data = [model_to_dict(hall_machine) for hall_machine in hall_machines]
            return JsonResponse(data, safe=False)

    def post(self, request, gym_id, hall_id):
        try:
            data = json.loads(request.body)
            hall_machine = HallMachineComponents().add_hall_machine(
                gym_id, hall_id, data
            )
            response_data = model_to_dict(hall_machine)
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, gym_id, hall_id, machine_id):
        try:
            data = json.loads(request.body)
            hall_machine = HallMachineComponents().modify_hall_machine(
                gym_id, hall_id, machine_id, data
            )
            response_data = model_to_dict(hall_machine)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Http404:
            return JsonResponse({"error": "HallMachine not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, gym_id, hall_id, machine_id):
        try:
            HallMachineComponents().remove_hall_machine(gym_id, hall_id, machine_id)
            return JsonResponse({"message": "Deleted successfully"}, status=204)
        except Http404:
            return JsonResponse({"error": "HallMachine not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
