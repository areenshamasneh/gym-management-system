import json
from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import MemberComponent
from gym_app.forms import MemberForm


@method_decorator(csrf_exempt, name="dispatch")
class MemberController(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component = MemberComponent()

    def get(self, request, gym_id, pk=None):
        if pk:
            member = self.component.fetch_member_by_id(gym_id, pk)
            data = model_to_dict(member)
            return JsonResponse(data)
        else:
            name_filter = request.GET.get("name", None)
            all_members = self.component.fetch_all_members(gym_id)

            if name_filter:
                filtered_members = [
                    member
                    for member in all_members
                    if name_filter.lower() in member.name.lower()
                ]
            else:
                filtered_members = all_members

            data = [model_to_dict(member) for member in filtered_members]
            return JsonResponse(data, safe=False)

    def post(self, request, gym_id):
        data = json.loads(request.body)
        form = MemberForm(data)
        if form.is_valid():
            member = self.component.add_member(gym_id, form.cleaned_data)
            response_data = model_to_dict(member)
            return JsonResponse(response_data, status=201)
        else:
            errors = {
                field: [e for e in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse(
                {"error": "Invalid data", "details": errors}, status=400
            )

    def put(self, request, gym_id, pk):
        data = json.loads(request.body)
        form = MemberForm(data)
        if form.is_valid():
            member = self.component.modify_member(gym_id, pk, form.cleaned_data)
            response_data = model_to_dict(member)
            return JsonResponse(response_data, status=200)
        else:
            errors = {
                field: [e for e in error_list]
                for field, error_list in form.errors.items()
            }
            return JsonResponse(
                {"error": "Invalid data", "details": errors}, status=400
            )

    def delete(self, request, gym_id, pk):
        self.component.remove_member(gym_id, pk)
        return JsonResponse({"message": "Deleted successfully"}, status=204)
