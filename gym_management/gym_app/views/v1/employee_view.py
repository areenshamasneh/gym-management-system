from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from gym_app.exceptions import ResourceNotFoundException, InvalidInputException
from gym_app.components import EmployeeComponent
from gym_app.models import Gym
from gym_app.serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        self.employee_component = EmployeeComponent()
        super().__init__(**kwargs)

    def list(self, request, gym_id=None):
        name = request.query_params.get("name", "")
        email = request.query_params.get("email", "")
        phone_number = request.query_params.get("phone_number", "")
        address_city = request.query_params.get("address_city", "")
        address_street = request.query_params.get("address_street", "")
        manager_id = request.query_params.get("manager_id", "")
        positions = request.query_params.get("positions", "")

        filter_criteria = {}
        if name:
            filter_criteria["name__icontains"] = name
        if email:
            filter_criteria["email__icontains"] = email
        if phone_number:
            filter_criteria["phone_number__icontains"] = phone_number
        if address_city:
            filter_criteria["address_city__icontains"] = address_city
        if address_street:
            filter_criteria["address_street__icontains"] = address_street
        if manager_id:
            filter_criteria["manager_id"] = manager_id
        if positions:
            filter_criteria["positions__icontains"] = positions

        try:
            employees = self.employee_component.fetch_all_employees(gym_id).filter(
                **filter_criteria
            )
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data)
        except InvalidInputException as e:
            return Response({"errors": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def retrieve(self, request, gym_id=None, pk=None):
        try:
            employee = self.employee_component.fetch_employee_by_id(gym_id, pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, gym_id=None):
        # Validate that gym_id is provided in URL and exists
        if gym_id is None:
            return Response(
                {"detail": "Gym ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            return Response(
                {"detail": f"Gym with ID {gym_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data.copy()
        data['gym'] = gym_id  # Include gym_id in the data for serializer

        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            try:
                # Add employee using EmployeeComponent
                employee = self.employee_component.add_employee(
                    gym_id, serializer.validated_data
                )
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except InvalidInputException as e:
                return Response(
                    {"detail": str(e)},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except Exception as e:
                return Response(
                    {"detail": "An unexpected error occurred."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, gym_id=None, pk=None):
        serializer = EmployeeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                employee = self.employee_component.modify_employee(
                    gym_id, pk, serializer.validated_data
                )
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data)
            except ResourceNotFoundException as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except InvalidInputException as e:
                return Response({"errors": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, gym_id=None, pk=None):
        serializer = EmployeeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                employee = self.employee_component.modify_employee(
                    gym_id, pk, serializer.validated_data
                )
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data)
            except ResourceNotFoundException as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except InvalidInputException as e:
                return Response({"errors": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, gym_id=None, pk=None):
        try:
            self.employee_component.remove_employee(gym_id, pk)
            return Response(
                {"message": "Employee deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidInputException as e:
            return Response({"errors": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
