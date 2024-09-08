from rest_framework import status, viewsets  # type: ignore
from rest_framework.response import Response  # type: ignore

from gym_app.components import AdminComponent
from gym_app.serializers import AdminSerializer
from gym_app.utils import PaginationResponse
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

        page_number = int(request.GET.get('page_number', 1))
        page_size = int(request.GET.get('page_size', 10))
        offset = (page_number - 1) * page_size

        admins, total_admins = self.admin_component.fetch_all_admins(gym_pk, filter_criteria, offset, page_size)

        pagination_response = PaginationResponse(
            items=self.schema.dump(admins, many=True),
            total_items=total_admins,
            current_page=page_number,
            page_size=page_size
        )

        return Response(pagination_response.to_dict(), status=status.HTTP_200_OK)

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
        return Response({"message": "Admin deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
