from gym_app.components.admin_component import AdminComponent
from gym_app.models.system_models import Gym
from rest_framework import viewsets  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from gym_app.serializers import AdminSerializer
from gym_app.exceptions import (
    ResourceNotFoundException,
    InvalidInputException,
    ConflictException,
)


class AdminViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        self.admin_component = AdminComponent()
        super().__init__(**kwargs)

    def list(self, request, gym_id=None):
        if gym_id is None:
            return Response(
                {"detail": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            return Response(
                {"detail": f"Gym with ID {gym_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        name = request.GET.get("name", "")
        email = request.GET.get("email", "")
        phone_number = request.GET.get("phone_number", "")
        address_city = request.GET.get("address_city", "")
        address_street = request.GET.get("address_street", "")

        filter_criteria = {
            "name__icontains": name,
            "email__icontains": email,
            "phone_number__icontains": phone_number,
            "address_city__icontains": address_city,
            "address_street__icontains": address_street,
        }
        filter_criteria = {k: v for k, v in filter_criteria.items() if v}

        try:
            admins = self.admin_component.fetch_all_admins(gym_id)
            filtered_admins = admins.filter(**filter_criteria)
            serializer = AdminSerializer(filtered_admins, many=True)
            return Response(serializer.data)
        except ConflictException as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None, gym_id=None):
        if gym_id is None:
            return Response(
                {"detail": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            return Response(
                {"detail": f"Gym with ID {gym_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            admin = self.admin_component.fetch_admin_by_id(gym_id, pk)
            serializer = AdminSerializer(admin)
            return Response(serializer.data)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ConflictException as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, gym_id=None):
        if gym_id is None:
            return Response(
                {"detail": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            return Response(
                {"detail": f"Gym with ID {gym_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        data = request.data.copy()
        data["gym_id"] = gym.id

        try:
            admin = self.admin_component.add_admin(gym.id, data)
            serializer = AdminSerializer(admin)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, pk=None, gym_id=None):
        if gym_id is None:
            return Response(
                {"detail": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data["gym_id"] = gym_id

        try:
            admin = self.admin_component.modify_admin(gym_id, pk, data)
            serializer = AdminSerializer(admin)
            return Response(serializer.data)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def partial_update(self, request, pk=None, gym_id=None):
        if gym_id is None:
            return Response(
                {"detail": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data.copy()
        data["gym_id"] = gym_id

        try:
            admin = self.admin_component.modify_admin(gym_id, pk, data)
            serializer = AdminSerializer(admin)
            return Response(serializer.data)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def destroy(self, request, pk=None, gym_id=None):
        if gym_id is None:
            return Response(
                {"detail": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            self.admin_component.remove_admin(gym_id, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"detail": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
