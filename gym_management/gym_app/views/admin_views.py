import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import (
    fetch_all_admins,
    fetch_admin_by_id,
    add_admin,
    modify_admin,
    remove_admin,
)


@method_decorator(csrf_exempt, name="dispatch")
class AdminListView(View):
    def get(self, request):
        admins = fetch_all_admins()
        data = [model_to_dict(admin) for admin in admins]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdminDetailView(View):
    def get(self, request, pk):
        admin = fetch_admin_by_id(pk)
        data = model_to_dict(admin)
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class AdminCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            admin = add_admin(data)
            response_data = model_to_dict(admin)
            return JsonResponse(response_data, status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Creation failed"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class AdminUpdateView(View):
    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            admin = modify_admin(pk, data)
            response_data = model_to_dict(admin)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class AdminDeleteView(View):
    def delete(self, request, pk):
        try:
            remove_admin(pk)
            return JsonResponse({"message": "Admin deleted"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
