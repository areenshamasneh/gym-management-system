from rest_framework import status, viewsets  # type: ignore
from rest_framework.response import Response  # type: ignore

from gym_app.components import GymComponent
from gym_app.serializers import GymSchema
from gym_app.utils import PaginationResponse
from gym_app.validators import SchemaValidator


class GymController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gym_component = GymComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.gym_schemas')
        self.gym_schema = GymSchema()

    def list(self, request):
        page_number = int(request.GET.get('page_number', 1))
        page_size = int(request.GET.get('page_size', 10))
        offset = (page_number - 1) * page_size

        gyms, total_gyms = self.gym_component.fetch_all_gyms(offset, page_size)

        pagination_response = PaginationResponse(
            items=self.gym_schema.dump(gyms, many=True),
            total_items=total_gyms,
            current_page=page_number,
            page_size=page_size
        )

        return Response(pagination_response.to_dict(), status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        gym = self.gym_component.fetch_gym_by_id(pk)
        serialized_gym = self.gym_schema.dump(gym)
        return Response(serialized_gym, status=status.HTTP_200_OK)

    def create(self, request):
        validation_error = self.validator.validate_data('CREATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        gym_data = request.data
        gym = self.gym_component.add_gym(gym_data)
        serialized_gym = self.gym_schema.dump(gym)
        return Response(serialized_gym, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        validation_error = self.validator.validate_data('UPDATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        gym_data = request.data
        updated_gym = self.gym_component.modify_gym(pk, gym_data)
        serialized_gym = self.gym_schema.dump(updated_gym)
        return Response(serialized_gym, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        self.gym_component.remove_gym(pk)
        return Response({"message": "Gym deleted successfully"}, status=status.HTTP_204_NO_CONTENT)