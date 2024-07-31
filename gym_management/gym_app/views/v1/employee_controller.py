from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import EmployeeComponent
from gym_app.forms import EmployeeForm
from gym_app.decorators import handle_exceptions
import json
from django.db.models import Q


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeController(View):
    def __init__(self):
        self.employee_component = EmployeeComponent()

    @handle_exceptions
    def get(self, request, gym_id, pk=None):
        name = request.GET.get("name", "")
        email = request.GET.get("email", "")
        phone_number = request.GET.get("phone_number", "")
        address_city = request.GET.get("address_city", "")
        address_street = request.GET.get("address_street", "")
        manager_id = request.GET.get("manager_id", "")
        positions = request.GET.get("positions", "")

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
        if manager_id:
            filter_criteria &= Q(manager_id=manager_id)
        if positions:
            filter_criteria &= Q(positions__icontains=positions)

        if pk:
            employee = self.employee_component.fetch_employee_by_id(gym_id, pk)
            data = model_to_dict(employee)
        else:
            employees = self.employee_component.fetch_all_employees(gym_id).filter(
                filter_criteria
            )
            data = [model_to_dict(employee) for employee in employees]

        return JsonResponse(data, safe=False)

    @handle_exceptions
    def post(self, request, gym_id):
        data = json.loads(request.body)
        form = EmployeeForm(data)
        if form.is_valid():
            employee_data = form.cleaned_data
            employee = self.employee_component.add_employee(gym_id, employee_data)
            response_data = model_to_dict(employee)
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    @handle_exceptions
    def put(self, request, gym_id, pk):
        data = json.loads(request.body)
        form = EmployeeForm(data)
        if form.is_valid():
            employee_data = form.cleaned_data
            employee = self.employee_component.modify_employee(
                gym_id, pk, employee_data
            )
            response_data = model_to_dict(employee)
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    @handle_exceptions
    def delete(self, request, gym_id, pk=None):
        if pk is None:
            return JsonResponse(
                {"error": "Primary key (pk) is required for deletion"}, status=400
            )

        self.employee_component.remove_employee(gym_id, pk)
        return JsonResponse({"message": "Employee deleted successfully"}, status=204)
