import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..models import HallMachine, Gym, Hall, Machine
from django.forms.models import model_to_dict


class HallMachineListView(View):
    def get(self, request):
        hall_machines = HallMachine.objects.all()
        data = [model_to_dict(hall_machine) for hall_machine in hall_machines]
        return JsonResponse(data, safe=False)


class HallMachineDetailView(View):
    def get(self, request, pk):
        hall_machine = get_object_or_404(HallMachine, pk=pk)
        data = model_to_dict(hall_machine)
        return JsonResponse(data)

@method_decorator(csrf_exempt, name="dispatch")
class HallMachineCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            hall_instance = get_object_or_404(Hall, pk=data.get("hall"))
            machine_instance = get_object_or_404(Machine, pk=data.get("machine"))

            if not hall_instance:
                return JsonResponse({"error": "Hall instance not found"}, status=400)
            if not machine_instance:
                return JsonResponse({"error": "Machine instance not found"}, status=400)

            hall_machine = HallMachine.objects.create(
                hall=hall_instance,
                machine=machine_instance,
                name=data.get("name"),
                uid=data.get("uid"),
            )

            return JsonResponse(model_to_dict(hall_machine), status=201)
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

            hall_machine = get_object_or_404(HallMachine, pk=pk)

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

            return JsonResponse(model_to_dict(hall_machine))
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
            hall_machine = get_object_or_404(HallMachine, pk=pk)
            hall_machine.delete()
            return JsonResponse(
                {"message": "HallMachine deleted successfully"}, status=204
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
