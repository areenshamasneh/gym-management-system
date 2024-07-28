import json
from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components.member_component import MemberComponent
from gym_app.models import Gym


@method_decorator(csrf_exempt, name="dispatch")
class MemberController(View):
    def get(self, request, pk=None):
        if pk:
            try:
                member = MemberComponent.fetch_member_by_id(pk)
                data = model_to_dict(member)
                return JsonResponse(data)
            except Http404:
                return JsonResponse({"error": "Member not found"}, status=404)
        else:
            members = MemberComponent.fetch_all_members()
            data = [model_to_dict(member) for member in members]
            return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            member = MemberComponent.add_member(data)
            response_data = model_to_dict(member)
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            member = MemberComponent.modify_member(pk, data)
            response_data = model_to_dict(member)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Http404:
            return JsonResponse({"error": "Member not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, pk):
        try:
            MemberComponent.remove_member(pk)
            return JsonResponse({"message": "Deleted successfully"}, status=204)
        except Http404:
            return JsonResponse({"error": "Member not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
