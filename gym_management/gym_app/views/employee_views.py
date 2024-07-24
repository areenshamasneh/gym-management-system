import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components.employee_component import (
    fetch_all_employees,
    fetch_employee_by_id,
    add_employee,
    modify_employee,
    remove_employee,
)


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeListView(View):
    def get(self, request):
        employees = fetch_all_employees()
        data = [model_to_dict(employee) for employee in employees]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeDetailView(View):
    def get(self, request, pk):
        employee = fetch_employee_by_id(pk)
        data = model_to_dict(employee)
        return JsonResponse(data)

    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            employee = modify_employee(pk, data)
            response_data = model_to_dict(employee)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, pk):
        try:
            remove_employee(pk)
            return JsonResponse(
                {"message": "Employee deleted successfully"}, status=204
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            employee = add_employee(data)
            response_data = model_to_dict(employee)
            return JsonResponse(response_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Creation failed", "details": str(e)}, status=500
            )


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeUpdateView(View):
    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            employee = modify_employee(pk, data)
            response_data = model_to_dict(employee)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeDeleteView(View):
    def delete(self, request, pk):
        try:
            remove_employee(pk)
            return JsonResponse(
                {"message": "Employee deleted successfully"}, status=204
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
