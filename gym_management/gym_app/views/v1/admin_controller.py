import json
from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from gym_app.components import AdminComponent
from gym_app.forms import AdminForm
from gym_app.decorators import handle_exceptions


@method_decorator(csrf_exempt, name="dispatch")
class AdminController(View):
    def __init__(self):
        self.admin_component = AdminComponent()

    @handle_exceptions
    def get(self, request, gym_id, pk=None):
        name = request.GET.get("name", "")
        email = request.GET.get("email", "")
        phone_number = request.GET.get("phone_number", "")
        address_city = request.GET.get("address_city", "")
        address_street = request.GET.get("address_street", "")

        filter_criteria = Q(gym_id=gym_id)
        if name:
            filter_criteria &= Q(name__icontains=name)
        if email:
            filter_criteria &= Q(email__icontains=email)
        if phone_number:
            filter_criteria &= Q(phone_number__icontains=phone_number)
        if address_city:
            filter_criteria &= Q(address_city__icontains=address_city)
        if address_street:
            filter_criteria &= Q(address_street__icontains=address_street)

        if pk is not None:
            admin = self.admin_component.fetch_admin_by_id(gym_id, pk)
            data = model_to_dict(admin)
        else:
            admins = self.admin_component.fetch_all_admins(gym_id).filter(
                filter_criteria
            )
            data = [model_to_dict(admin) for admin in admins]
        return JsonResponse(data, safe=False)

    @handle_exceptions
    def post(self, request, gym_id):
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

    @handle_exceptions
    def put(self, request, gym_id, pk):
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

    @handle_exceptions
    def delete(self, request, gym_id, pk):
        self.admin_component.remove_admin(gym_id, pk)
        return JsonResponse({}, status=204)
