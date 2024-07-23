from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ..models import Employee, Gym
from django.forms.models import model_to_dict
import json


class EmployeeListView(View):
    def get(self, request):
        employees = Employee.objects.all()
        data = [model_to_dict(employee) for employee in employees]
        return JsonResponse(data, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class EmployeeDetailView(View):
    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        data = model_to_dict(employee)
        return JsonResponse(data)

    def put(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        try:
            data = json.loads(request.body)
            for attr, value in data.items():
                setattr(employee, attr, value)
            employee.save()
            return JsonResponse(model_to_dict(employee))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            return JsonResponse({"error": "Update failed"}, status=500)

    def delete(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk)
        try:
            employee.delete()
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
            gym_id = data.get("gym")
            if gym_id is not None:
                gym_instance = get_object_or_404(Gym, pk=gym_id)
                data["gym"] = gym_instance
            else:
                return JsonResponse({"error": "Gym field is required"}, status=400)

            employee = Employee.objects.create(**data)
            return JsonResponse(model_to_dict(employee), status=201)
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
            employee = get_object_or_404(Employee, pk=pk)

            for attr, value in data.items():
                if attr == "gym":
                    if value:
                        gym_instance = get_object_or_404(Gym, pk=value)
                        setattr(employee, attr, gym_instance)
                else:
                    setattr(employee, attr, value)

            employee.save()
            return JsonResponse(model_to_dict(employee))
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
            employee = get_object_or_404(Employee, pk=pk)
            employee.delete()
            return JsonResponse(
                {"message": "Employee deleted successfully"}, status=204
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
