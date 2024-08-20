from rest_framework import status, viewsets
from rest_framework.response import Response

from gym_app.components.admin_component import AdminComponent
from gym_app.exceptions import ResourceNotFoundException, InvalidInputException, ConflictException
from gym_app.serializers import AdminSerializer
from gym_app.validators import SchemaValidator


class AdminViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.admin_component = AdminComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.schemas.admin_schemas')

    def list(self, request, gym_pk=None):
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
            admins = self.admin_component.fetch_all_admins(gym_pk)
            if filter_criteria:
                admins = admins.filter(**filter_criteria)
            serializer = AdminSerializer(admins, many=True)
            return Response(serializer.data)
        except ConflictException as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, gym_pk=None, pk=None):
        try:
            admin = self.admin_component.fetch_admin_by_id(gym_pk, pk)
            serializer = AdminSerializer(admin)
            return Response(serializer.data)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ConflictException as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, gym_pk=None):
        data = request.data.copy()
        data["gym_id"] = gym_pk

        validation_error = self.validator.validate_data('CREATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        try:
            admin = self.admin_component.add_admin(gym_pk, data)
            serializer = AdminSerializer(admin)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, gym_pk=None, pk=None):
        data = request.data.copy()
        data["gym_id"] = gym_pk

        validation_error = self.validator.validate_data('UPDATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        try:
            admin = self.admin_component.modify_admin(gym_pk, pk, data)
            serializer = AdminSerializer(admin)
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
        try:
            self.admin_component.remove_admin(gym_pk, pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
