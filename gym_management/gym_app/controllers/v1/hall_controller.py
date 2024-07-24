import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import (
    fetch_all_halls,
    fetch_hall_by_id,
    add_hall,
    modify_hall,
    remove_hall,
)
from gym_app.models import HallType, Gym


@method_decorator(csrf_exempt, name="dispatch")
class HallListView(View):
    def get(self, request):
        halls = fetch_all_halls()
        data = [model_to_dict(hall) for hall in halls]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class HallDetailView(View):
    def get(self, request, pk):
        hall = fetch_hall_by_id(pk)
        data = model_to_dict(hall)
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class HallCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            hall = add_hall(data)
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
    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            hall = modify_hall(pk, data)
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
    def delete(self, request, pk):
        try:
            remove_hall(pk)
            return JsonResponse({"message": "Hall deleted"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
