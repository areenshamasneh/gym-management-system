import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components.admin_component import AdminComponent


@method_decorator(csrf_exempt, name="dispatch")
class AdminController(View):
    def get(self, request, pk=None):
        if pk:
            admin = AdminComponent.fetch_admin_by_id(pk)
            data = model_to_dict(admin)
        else:
            admins = AdminComponent.fetch_all_admins()
            data = [model_to_dict(admin) for admin in admins]
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            admin = AdminComponent.add_admin(data)
            response_data = model_to_dict(admin)
            return JsonResponse(response_data, status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Creation failed"}, status=500)

    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            admin = AdminComponent.modify_admin(pk, data)
            response_data = model_to_dict(admin)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, pk=None):
        if pk is None:
            return JsonResponse({"error": "Primary key (pk) is required for deletion"}, status=400)

        try:
            AdminComponent.remove_admin(pk)
            return JsonResponse({"message": "Admin deleted"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)