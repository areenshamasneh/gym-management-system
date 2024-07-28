import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import EmployeeComponent


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeController(View):
    def get(self, request, pk=None):
        if pk:
            employee = EmployeeComponent.fetch_employee_by_id(pk)
            data = model_to_dict(employee)
        else:
            employees = EmployeeComponent.fetch_all_employees()
            data = [model_to_dict(employee) for employee in employees]
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            employee = EmployeeComponent.add_employee(data)
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

    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            employee = EmployeeComponent.modify_employee(pk, data)
            response_data = model_to_dict(employee)
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Update failed", "details": str(e)}, status=500
            )

    def delete(self, request, pk=None):
        if pk is None:
            return JsonResponse(
                {"error": "Primary key (pk) is required for deletion"}, status=400
            )

        try:
            EmployeeComponent.remove_employee(pk)
            return JsonResponse(
                {"message": "Employee deleted successfully"}, status=204
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
