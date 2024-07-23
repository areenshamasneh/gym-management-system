import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components.hall_component import (
    get_all_halls,
    get_hall_by_id,
    create_hall,
    update_hall,
    delete_hall,
)
from gym_app.models.system_models import HallType, Gym


@method_decorator(csrf_exempt, name="dispatch")
class HallListView(View):
    def get(self, request):
        halls = get_all_halls()
        data = [model_to_dict(hall) for hall in halls]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class HallDetailView(View):
    def get(self, request, pk):
        hall = get_hall_by_id(pk)
        data = model_to_dict(hall)
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class HallCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            hall = create_hall(data)
            response_data = model_to_dict(hall)
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except HallType.DoesNotExist:
            return JsonResponse({"error": "Invalid HallType ID"}, status=400)
        except Gym.DoesNotExist:
            return JsonResponse({"error": "Invalid Gym ID"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class HallUpdateView(View):
    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            hall = update_hall(kwargs.get("pk"), data)
            response_data = model_to_dict(hall)
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except HallType.DoesNotExist:
            return JsonResponse({"error": "Invalid HallType ID"}, status=400)
        except Gym.DoesNotExist:
            return JsonResponse({"error": "Invalid Gym ID"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class HallDeleteView(View):
    def delete(self, request, pk, *args, **kwargs):
        delete_hall(pk)
        return JsonResponse({"message": "Hall deleted"}, status=204)
