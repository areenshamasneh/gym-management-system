from rest_framework import status, viewsets
from rest_framework.response import Response

from gym_app.components import EmployeeComponent
from gym_app.serializers import EmployeeSerializer
from gym_app.validators import SchemaValidator


class EmployeeController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.employee_component = EmployeeComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.employee_schemas')
        self.schema = EmployeeSerializer()

    def list(self, request, gym_pk=None):
        employees = self.employee_component.fetch_all_employees(gym_pk)
        serialized_employees = self.schema.dump(employees, many=True)
        return Response(serialized_employees)

    def retrieve(self, request, gym_pk=None, pk=None):
        employee = self.employee_component.fetch_employee_by_id(gym_pk, pk)
        serialized_employee = self.schema.dump(employee)
        return Response(serialized_employee)

    def create(self, request, gym_pk=None):
        data = request.data.copy()
        data["gym"] = {"id": gym_pk}

        validation_error = self.validator.validate_data('CREATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        employee = self.employee_component.add_employee(gym_pk, data)
        serialized_employee = self.schema.dump(employee)
        return Response(serialized_employee, status=status.HTTP_201_CREATED)

    def update(self, request, gym_pk=None, pk=None):
        data = request.data.copy()
        data["gym"] = {"id": gym_pk}

        validation_error = self.validator.validate_data('UPDATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        employee = self.employee_component.modify_employee(gym_pk, pk, data)
        serialized_employee = self.schema.dump(employee)
        return Response(serialized_employee)

    def partial_update(self, request, gym_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, pk=pk)

    def destroy(self, request, gym_pk=None, pk=None):
        self.employee_component.remove_employee(gym_pk, pk)
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
