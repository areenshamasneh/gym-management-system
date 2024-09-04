from rest_framework import status, viewsets
from rest_framework.response import Response

from gym_app.components import EmployeeComponent
from gym_app.exceptions import ResourceNotFoundException, InvalidInputException
from gym_app.serializers import EmployeeSerializer
from gym_app.validators import SchemaValidator


class EmployeeController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.employee_component = EmployeeComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.employee_schemas')
        self.schema = EmployeeSerializer()

    def list(self, request, gym_pk=None):
        try:
            employees = self.employee_component.fetch_all_employees(gym_pk)
            serialized_employees = self.schema.dump(employees, many=True)
            return Response(serialized_employees)
        except Exception as e:
            return Response({"detail": f"An unexpected error occurred. {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, gym_pk=None, pk=None):
        try:
            employee = self.employee_component.fetch_employee_by_id(gym_pk, pk)
            serialized_employee = self.schema.dump(employee)
            return Response(serialized_employee)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"An unexpected error occurred."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, gym_pk=None):
        data = request.data.copy()
        data["gym"] = {"id": gym_pk}

        validation_error = self.validator.validate_data('CREATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = self.employee_component.add_employee(gym_pk, data)
            serialized_employee = self.schema.dump(employee)
            return Response(serialized_employee, status=status.HTTP_201_CREATED)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, gym_pk=None, pk=None):
        data = request.data.copy()
        data["gym"] = {"id": gym_pk}

        validation_error = self.validator.validate_data('UPDATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = self.employee_component.modify_employee(gym_pk, pk, data)
            serialized_employee = self.schema.dump(employee)
            return Response(serialized_employee)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"An unexpected error occurred. {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, gym_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, pk=pk)

    def destroy(self, request, gym_pk=None, pk=None):
        try:
            self.employee_component.remove_employee(gym_pk, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
