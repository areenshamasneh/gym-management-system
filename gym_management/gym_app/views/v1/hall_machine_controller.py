import json
from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import HallMachineComponents
from gym_app.forms import HallMachineForm

@method_decorator(csrf_exempt, name="dispatch")
class HallMachineController(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component = HallMachineComponents()

    def get(self, request, gym_id, hall_id, machine_id=None):
        try:
            if machine_id:
                hall_machine = self.component.fetch_hall_machine_by_id(
                    gym_id, hall_id, machine_id
                )
                data = model_to_dict(hall_machine)
                return JsonResponse(data)
            else:
                hall_machines = self.component.fetch_all_hall_machines(gym_id, hall_id)
                data = [model_to_dict(hall_machine) for hall_machine in hall_machines]
                return JsonResponse(data, safe=False)
        except Http404:
            return JsonResponse({"error": "HallMachine not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request, gym_id, hall_id):
        try:
            data = json.loads(request.body)
            form = HallMachineForm(data)
            if form.is_valid():
                hall_machine = self.component.add_hall_machine(
                    gym_id, hall_id, form.cleaned_data
                )
                response_data = model_to_dict(hall_machine)
                return JsonResponse(response_data, status=201)
            else:
                return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
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
