import json
from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components.hall_component import HallComponent


@method_decorator(csrf_exempt, name="dispatch")
class HallController(View):
    def get(self, request, gym_id, pk=None):
        if pk:
            try:
                hall = HallComponent.fetch_hall_by_id(gym_id, pk)
                data = model_to_dict(hall)
                return JsonResponse(data)
            except Http404:
                return JsonResponse({"error": "Hall not found"}, status=404)
        else:
            halls = HallComponent.fetch_all_halls(gym_id)
            data = [model_to_dict(hall) for hall in halls]
            return JsonResponse(data, safe=False)

    def post(self, request, gym_id):
        try:
            data = json.loads(request.body)
            hall = HallComponent.add_hall(gym_id, data)
            response_data = model_to_dict(hall)
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Http404 as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, gym_id, pk):
        try:
            data = json.loads(request.body)
            hall = HallComponent.modify_hall(gym_id, pk, data)
            response_data = model_to_dict(hall)
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Http404:
            return JsonResponse({"error": "Hall not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, gym_id, pk):
        try:
            HallComponent.remove_hall(gym_id, pk)
            return JsonResponse({"message": "Hall deleted"}, status=204)
        except Http404:
            return JsonResponse({"error": "Hall not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
