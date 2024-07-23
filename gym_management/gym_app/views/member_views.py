from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import json
from ..models import Member, Gym


class MemberListView(View):
    def get(self, request):
        members = Member.objects.all()
        data = [model_to_dict(member) for member in members]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class MemberDetailView(View):
    def get(self, request, pk):
        member = get_object_or_404(Member, pk=pk)
        data = model_to_dict(member)
        return JsonResponse(data)

    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            member = get_object_or_404(Member, pk=pk)
            for attr, value in data.items():
                if hasattr(member, attr):
                    setattr(member, attr, value)
            member.save()
            return JsonResponse(model_to_dict(member))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, pk):
        try:
            member = get_object_or_404(Member, pk=pk)
            member.delete()
            return JsonResponse({"message": "Deleted successfully"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class MemberCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if "gym" in data:
                gym_id = data.pop("gym")
                data["gym"] = get_object_or_404(Gym, pk=gym_id)
            member = Member.objects.create(**data)
            return JsonResponse(model_to_dict(member), status=201)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Creation failed"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class MemberUpdateView(View):
    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            member = get_object_or_404(Member, pk=pk)

            if "gym" in data:
                gym_id = data.pop("gym")
                data["gym"] = get_object_or_404(Gym, pk=gym_id)

            for attr, value in data.items():
                if hasattr(member, attr):
                    setattr(member, attr, value)
            member.save()
            return JsonResponse(model_to_dict(member))
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
            member = get_object_or_404(Member, pk=pk)
            member.delete()
            return JsonResponse({"message": "Deleted successfully"}, status=204)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
