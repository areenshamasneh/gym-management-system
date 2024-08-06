from rest_framework import status, viewsets
from rest_framework.response import Response

from gym_app.components import EmployeeComponent
from gym_app.exceptions import ResourceNotFoundException, InvalidInputException
from gym_app.models import Gym
from gym_app.serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        self.employee_component = EmployeeComponent()
        super().__init__(**kwargs)

    @staticmethod
    def get_gym(gym_id):
        try:
            return Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            raise ResourceNotFoundException(f"Gym with ID {gym_id} does not exist")

    def list(self, request, gym_pk=None):
        self.get_gym(gym_pk)

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
            employees = self.employee_component.fetch_all_employees(gym_pk).filter(
                **filter_criteria
            )
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data)
        except InvalidInputException as e:
            return Response({"errors": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(f"Unexpected error occurred in list: {e}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def retrieve(self, request, gym_pk=None, pk=None):
        self.get_gym(gym_pk)

        try:
            employee = self.employee_component.fetch_employee_by_id(gym_pk, pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error occurred in retrieve: {e}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def create(self, request, gym_pk=None):
        self.get_gym(gym_pk)

        data = request.data.copy()
        data['gym'] = gym_pk

        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            try:
                employee = self.employee_component.add_employee(
                    gym_pk, serializer.validated_data
                )
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except InvalidInputException as e:
                return Response(
                    {"detail": str(e)},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except Exception as e:
                print(f"Unexpected error occurred in create: {e}")
                return Response(
                    {"detail": "An unexpected error occurred."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, gym_pk=None, pk=None):
        self.get_gym(gym_pk)

        serializer = EmployeeSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                employee = self.employee_component.modify_employee(
                    gym_pk, pk, serializer.validated_data
                )
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data)
            except ResourceNotFoundException as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except InvalidInputException as e:
                return Response({"errors": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            except Exception as e:
                print(f"Unexpected error occurred in update: {e}")
                return Response(
                    {"detail": "An unexpected error occurred."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, gym_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, pk=pk)

    def destroy(self, request, gym_pk=None, pk=None):
        self.get_gym(gym_pk)

        try:
            self.employee_component.remove_employee(gym_pk, pk)
            return Response(
                {"message": "Employee deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidInputException as e:
            return Response({"errors": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            print(f"Unexpected error occurred in destroy: {e}")
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
