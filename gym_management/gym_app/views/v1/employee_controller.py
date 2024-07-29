import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import EmployeeComponent
from gym_app.forms import EmployeeForm


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeController(View):
    def __init__(self):
        self.employee_component = EmployeeComponent()

    def get(self, request, gym_id, pk=None):
        try:
            if pk:
                employee = self.employee_component.fetch_employee_by_id(gym_id, pk)
                data = model_to_dict(employee)
            else:
                employees = self.employee_component.fetch_all_employees(gym_id)
                data = [model_to_dict(employee) for employee in employees]
            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def post(self, request, gym_id):
        try:
            data = json.loads(request.body)
            form = EmployeeForm(data)
            if form.is_valid():
                employee_data = form.cleaned_data
                employee = self.employee_component.add_employee(gym_id, employee_data)
                response_data = model_to_dict(employee)
                return JsonResponse(response_data, status=201)
            else:
                errors = form.errors.as_json()
                return JsonResponse(
                    {"error": f"Form validation errors: {errors}"}, status=400
                )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Creation failed: {str(e)}"}, status=500)

    def put(self, request, gym_id, pk):
        try:
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
                errors = form.errors.as_json()
                return JsonResponse(
                    {"error": f"Form validation errors: {errors}"}, status=400
                )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
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
            self.employee_component.remove_employee(gym_id, pk)
            return JsonResponse(
                {"message": "Employee deleted successfully"}, status=204
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
