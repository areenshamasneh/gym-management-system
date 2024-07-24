import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import (
    fetch_all_members,
    fetch_member_by_id,
    add_member,
    modify_member,
    remove_member,
)


@method_decorator(csrf_exempt, name="dispatch")
class MemberListView(View):
    def get(self, request):
        members = fetch_all_members()
        data = [model_to_dict(member) for member in members]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class MemberDetailView(View):
    def get(self, request, pk):
        member = fetch_member_by_id(pk)
        data = model_to_dict(member)
        return JsonResponse(data)

    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            member = modify_member(pk, data)
            response_data = model_to_dict(member)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, pk):
        try:
            remove_member(pk)
            return JsonResponse({"message": "Deleted successfully"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class MemberCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            member = add_member(data)
            response_data = model_to_dict(member)
            return JsonResponse(response_data, status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Creation failed", "details": str(e)}, status=500
            )


@method_decorator(csrf_exempt, name="dispatch")
class MemberUpdateView(View):
    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            member = modify_member(pk, data)
            response_data = model_to_dict(member)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class MemberDeleteView(View):
    def delete(self, request, pk):
        try:
            remove_member(pk)
            return JsonResponse({"message": "Deleted successfully"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
