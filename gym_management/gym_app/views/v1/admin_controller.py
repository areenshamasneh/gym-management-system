import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components.admin_component import AdminComponent


@method_decorator(csrf_exempt, name="dispatch")
class AdminController(View):

    def get(self, request, gym_id, pk=None):
        try:
            if pk:
                admin = AdminComponent.fetch_admin_by_id(gym_id, pk)
                data = model_to_dict(admin)
            else:
                admins = AdminComponent.fetch_all_admins(gym_id)
                data = [model_to_dict(admin) for admin in admins]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request, gym_id):
        try:
            data = json.loads(request.body)
            admin = AdminComponent.add_admin(gym_id, data)
            response_data = model_to_dict(admin)
            return JsonResponse(response_data, status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            # Logging detailed exception
            return JsonResponse({"error": f"Creation failed: {str(e)}"}, status=500)

    def put(self, request, gym_id, pk):
        try:
            data = json.loads(request.body)
            admin = AdminComponent.modify_admin(gym_id, pk, data)
            response_data = model_to_dict(admin)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            # Logging detailed exception
            return JsonResponse({"error": f"Update failed: {str(e)}"}, status=500)

    def delete(self, request, gym_id, pk=None):
        if pk is None:
            return JsonResponse(
                {"error": "Primary key (pk) is required for deletion"}, status=400
            )
        try:
            AdminComponent.remove_admin(gym_id, pk)
            return JsonResponse({"message": "Admin deleted"}, status=204)
        except Exception as e:
            # Logging detailed exception
            return JsonResponse({"error": str(e)}, status=400)
