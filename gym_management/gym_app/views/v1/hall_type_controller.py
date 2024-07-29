import json
from django.forms import model_to_dict
from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gym_app.components import HallTypeComponent
from gym_app.forms.hall_type import HallTypeForm

@method_decorator(csrf_exempt, name="dispatch")
class HallTypeController(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component = HallTypeComponent()

    def get(self, request, hall_type_id=None):
        try:
            if hall_type_id:
                hall_type = self.component.fetch_hall_type_by_id(hall_type_id)
                data = model_to_dict(hall_type)
                return JsonResponse(data)
            else:
                hall_types = self.component.fetch_all_hall_types()
                data = [model_to_dict(hall_type) for hall_type in hall_types]
                return JsonResponse(data, safe=False)
        except Http404:
            return JsonResponse({"error": "HallType not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            form = HallTypeForm(data)
            if form.is_valid():
                hall_type = self.component.add_hall_type(form.cleaned_data)
                response_data = model_to_dict(hall_type)
                return JsonResponse(response_data, status=201)
            else:
                return JsonResponse({"error": "Invalid data", "details": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Creation failed", "details": str(e)}, status=500)

    def put(self, request, hall_type_id, *args, **kwargs):
        try:
            data = json.loads(request.body)
            form = HallTypeForm(data)
            if form.is_valid():
                hall_type = self.component.modify_hall_type(hall_type_id, form.cleaned_data)
                response_data = model_to_dict(hall_type)
                return JsonResponse(response_data)
            else:
                return JsonResponse({"error": "Invalid data", "details": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Http404:
            return JsonResponse({"error": "HallType not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Update failed", "details": str(e)}, status=500)

    def delete(self, request, hall_type_id, *args, **kwargs):
        try:
            self.component.remove_hall_type(hall_type_id)
            return JsonResponse({"message": "HallType deleted successfully"}, status=204)
        except Http404:
            return JsonResponse({"error": "HallType not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Deletion failed", "details": str(e)}, status=500)
