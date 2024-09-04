from rest_framework import status, viewsets
from rest_framework.response import Response

from gym_app.components.admin_component import AdminComponent
from gym_app.exceptions import ResourceNotFoundException, InvalidInputException
from gym_app.serializers import AdminSerializer
from gym_app.validators import SchemaValidator


class AdminController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.admin_component = AdminComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.admin_schemas')
        self.schema = AdminSerializer()

    def list(self, request, gym_pk=None):
        filter_criteria = {
            "name": request.GET.get("name", ""),
            "email": request.GET.get("email", ""),
            "phone_number": request.GET.get("phone_number", ""),
            "address_city": request.GET.get("address_city", ""),
            "address_street": request.GET.get("address_street", ""),
        }
        admins = self.admin_component.fetch_all_admins(gym_pk, filter_criteria)
        serialized_admins = self.schema.dump(admins, many=True)
        return Response(serialized_admins)

    def retrieve(self, request, gym_pk=None, pk=None):
        admin = self.admin_component.fetch_admin_by_id(gym_pk, pk)
        serialized_admin = self.schema.dump(admin)
        return Response(serialized_admin)

    def create(self, request, gym_pk=None):
        data = request.data.copy()
        data["gym_id"] = gym_pk

        validation_error = self.validator.validate_data('CREATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        admin = self.admin_component.add_admin(gym_pk, data)
        serialized_admin = self.schema.dump(admin)
        return Response(serialized_admin, status=status.HTTP_201_CREATED)

    def update(self, request, gym_pk=None, pk=None):
        data = request.data.copy()
        data["gym_id"] = gym_pk

        validation_error = self.validator.validate_data('UPDATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        admin = self.admin_component.modify_admin(gym_pk, pk, data)
        serialized_admin = self.schema.dump(admin)
        return Response(serialized_admin)

    def partial_update(self, request, gym_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, pk=pk)

    def destroy(self, request, gym_pk=None, pk=None):
        self.admin_component.remove_admin(gym_pk, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
