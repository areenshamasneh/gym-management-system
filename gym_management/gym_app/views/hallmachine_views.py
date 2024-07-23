import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components.hallmachine_component import (
    get_all_hall_machines,
    get_hall_machine_by_id,
    create_hall_machine,
    update_hall_machine,
    delete_hall_machine
)

class HallMachineListView(View):
    def get(self, request):
        hall_machines = get_all_hall_machines()
        data = [model_to_dict(hall_machine) for hall_machine in hall_machines]
        return JsonResponse(data, safe=False)


class HallMachineDetailView(View):
    def get(self, request, pk):
        hall_machine = get_hall_machine_by_id(pk)
        data = model_to_dict(hall_machine)
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class HallMachineCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            hall_machine = create_hall_machine(data)
            response_data = model_to_dict(hall_machine)
            return JsonResponse(response_data, status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Creation failed: {str(e)}"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class HallMachineUpdateView(View):
    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            hall_machine = update_hall_machine(pk, data)
            response_data = model_to_dict(hall_machine)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Update failed: {str(e)}"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class HallMachineDeleteView(View):
    def delete(self, request, pk):
        try:
            delete_hall_machine(pk)
            return JsonResponse({"message": "HallMachine deleted successfully"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
