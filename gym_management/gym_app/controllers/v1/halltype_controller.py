import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import (
    fetch_all_hall_types,
    fetch_hall_type_by_id,
    add_hall_type,
    modify_hall_type,
    remove_hall_type,
)


@method_decorator(csrf_exempt, name="dispatch")
class HallTypeListView(View):
    def get(self, request):
        hall_types = fetch_all_hall_types()
        data = [model_to_dict(hall_type) for hall_type in hall_types]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class HallTypeDetailView(View):
    def get(self, request, pk):
        hall_type = fetch_hall_type_by_id(pk)
        data = model_to_dict(hall_type)
        return JsonResponse(data)

    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            hall_type = modify_hall_type(pk, data)
            response_data = model_to_dict(hall_type)
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, pk):
        try:
            remove_hall_type(pk)
            return JsonResponse({"message": "Deleted successfully"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class HallTypeCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            hall_type = add_hall_type(data)
            response_data = model_to_dict(hall_type)
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Creation failed"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class HallTypeUpdateView(View):
    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            hall_type = modify_hall_type(pk, data)
            response_data = model_to_dict(hall_type)
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class HallTypeDeleteView(View):
    def delete(self, request, pk):
        try:
            remove_hall_type(pk)
            return JsonResponse(
                {"message": "HallType deleted successfully"}, status=204
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
