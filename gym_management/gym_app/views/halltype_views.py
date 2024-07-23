from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..models import HallType
from django.forms.models import model_to_dict
import json


class HallTypeListView(View):
    def get(self, request):
        hall_types = HallType.objects.all()
        data = [model_to_dict(hall_type) for hall_type in hall_types]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class HallTypeDetailView(View):
    def get(self, request, pk):
        hall_type = get_object_or_404(HallType, pk=pk)
        data = model_to_dict(hall_type)
        return JsonResponse(data)

    def put(self, request, pk):
        hall_type = get_object_or_404(HallType, pk=pk)
        try:
            data = json.loads(request.body)
            for attr, value in data.items():
                setattr(hall_type, attr, value)
            hall_type.save()
            return JsonResponse(model_to_dict(hall_type))
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, pk):
        hall_type = get_object_or_404(HallType, pk=pk)
        hall_type.delete()
        return JsonResponse({"message": "Deleted successfully"}, status=204)


@method_decorator(csrf_exempt, name="dispatch")
class HallTypeUpdateView(View):
    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            hall_type = get_object_or_404(HallType, pk=pk)
            for attr, value in data.items():
                setattr(hall_type, attr, value)
            hall_type.save()
            return JsonResponse(model_to_dict(hall_type))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class HallTypeCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            hall_type = HallType.objects.create(**data)
            return JsonResponse(model_to_dict(hall_type), status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Creation failed"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class HallTypeDeleteView(View):
    def delete(self, request, pk):
        try:
            hall_type = get_object_or_404(HallType, pk=pk)
            hall_type.delete()
            return JsonResponse(
                {"message": "HallType deleted successfully"}, status=204
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
