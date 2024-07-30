from django.forms import model_to_dict
from django.http import JsonResponse
import json
from django.views import View
from gym_app.components import AdminComponent
from gym_app.forms import AdminForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name="dispatch")
class AdminController(View):
    def __init__(self):
        self.admin_component = AdminComponent()

    def get(self, request, gym_id, pk=None):
        try:
            if pk is not None:
                admin = self.admin_component.fetch_admin_by_id(gym_id, pk)
                data = model_to_dict(admin)
            else:
                admins = self.admin_component.fetch_all_admins(gym_id)
                data = [model_to_dict(admin) for admin in admins]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request, gym_id):
        try:
            data = json.loads(request.body)
            form = AdminForm(data)
            if form.is_valid():
                admin_data = form.cleaned_data
                admin = self.admin_component.add_admin(gym_id, admin_data)
                response_data = model_to_dict(admin)
                return JsonResponse(response_data, status=201)
            else:
                errors = {field: errors for field, errors in form.errors.items()}
                return JsonResponse(
                    {"error": "Form validation errors", "details": errors}, status=400
                )
        except Exception as e:
            return JsonResponse({"error": f"Creation failed: {str(e)}"}, status=500)

    def put(self, request, gym_id, pk):
        try:
            data = json.loads(request.body)
            form = AdminForm(data)
            if form.is_valid():
                admin_data = form.cleaned_data
                admin = self.admin_component.modify_admin(gym_id, pk, admin_data)
                response_data = model_to_dict(admin)
                return JsonResponse(response_data, status=200)
            else:
                errors = {field: errors for field, errors in form.errors.items()}
                return JsonResponse(
                    {"error": "Form validation errors", "details": errors}, status=400
                )
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Update failed: {str(e)}"}, status=500)

    def delete(self, request, gym_id, pk=None):
        if pk is None:
            return JsonResponse(
                {"error": "Primary key (pk) is required for deletion"}, status=400
            )
        try:
            self.admin_component.remove_admin(gym_id, pk)
            return JsonResponse({"message": "Admin deleted"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
