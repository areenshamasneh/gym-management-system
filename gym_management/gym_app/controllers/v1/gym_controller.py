from rest_framework import status, viewsets  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status, viewsets
from rest_framework.response import Response

from common.cache_manager import CacheManager
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
        self.cache_manager = CacheManager(prefix='gym')

    def list(self, request):
        page_number = int(request.GET.get('page_number', 1))
        page_size = int(request.GET.get('page_size', 10))
        cache_key = f"list_{page_number}_{page_size}"

        cached_response = self.cache_manager.get(cache_key)
        if cached_response:
            return Response(cached_response, status=status.HTTP_200_OK)

        gyms, total_gyms = self.gym_component.fetch_all_gyms(page_number, page_size)
        pagination_response = PaginationResponse(
            items=self.gym_schema.dump(gyms, many=True),
            total_items=total_gyms,
            current_page=page_number,
            page_size=page_size
        ).to_dict()

        self.cache_manager.set(cache_key, pagination_response)

        return Response(pagination_response, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        cache_key = f"gym_{pk}"

        cached_gym = self.cache_manager.get(cache_key)
        if cached_gym:
            return Response(cached_gym, status=status.HTTP_200_OK)

        gym = self.gym_component.fetch_gym_by_id(pk)
        serialized_gym = self.gym_schema.dump(gym)

        self.cache_manager.set(cache_key, serialized_gym)

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
