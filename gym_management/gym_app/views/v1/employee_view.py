from rest_framework import status, viewsets
from rest_framework.response import Response

from gym_app.components import EmployeeComponent
from gym_app.exceptions import ResourceNotFoundException, InvalidInputException
from gym_app.models import Gym
from gym_app.serializers import EmployeeSerializer
from gym_app.validators import SchemaValidator


class EmployeeViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.employee_component = EmployeeComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.schemas.employee_schemas')

    @staticmethod
    def get_gym(gym_id):
        try:
            return Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            raise ResourceNotFoundException(f"Gym with ID {gym_id} does not exist")

    def list(self, request, gym_pk=None):
        self.get_gym(gym_pk)

        name = request.GET.get("name", "")
        email = request.GET.get("email", "")
        phone_number = request.GET.get("phone_number", "")
        address_city = request.GET.get("address_city", "")
        address_street = request.GET.get("address_street", "")
        manager_id = request.GET.get("manager_id", "")
        positions = request.GET.get("positions", "")

        filter_criteria = {
            "name__icontains": name,
            "email__icontains": email,
            "phone_number__icontains": phone_number,
            "address_city__icontains": address_city,
            "address_street__icontains": address_street,
            "manager_id": manager_id,
            "positions__icontains": positions,
        }
        filter_criteria = {k: v for k, v in filter_criteria.items() if v}

        try:
            employees = self.employee_component.fetch_all_employees(gym_pk).select_related('gym', 'manager')
            if filter_criteria:
                employees = employees.filter(**filter_criteria).select_related('gym', 'manager')

            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data)
        except Exception as e:
            return self.handle_exception(e)

    def retrieve(self, request, gym_pk=None, pk=None):
        self.get_gym(gym_pk)

        try:
            employee = self.employee_component.fetch_employee_by_id(gym_pk, pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Exception as e:
            return self.handle_exception(e)

    def create(self, request, gym_pk=None):
        self.get_gym(gym_pk)

        data = request.data.copy()
        data["gym"] = {"id": gym_pk}

        validation_error = self.validator.validate_data('CREATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = self.employee_component.add_employee(gym_pk, data)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, gym_pk=None, pk=None):
        self.get_gym(gym_pk)

        data = request.data.copy()
        data["gym"] = {"id": gym_pk}

        validation_error = self.validator.validate_data('UPDATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = self.employee_component.modify_employee(gym_pk, pk, data)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, gym_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, pk=pk)

    def destroy(self, request, gym_pk=None, pk=None):
        self.get_gym(gym_pk)

        try:
            self.employee_component.remove_employee(gym_pk, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
