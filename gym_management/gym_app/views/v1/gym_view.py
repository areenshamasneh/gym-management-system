from rest_framework import status, viewsets
from rest_framework.response import Response

from gym_app.components import GymComponent
from gym_app.serializers import serialize_gym
from gym_app.validators import SchemaValidator


class GymViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gym_component = GymComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.schemas.gym_schemas')

    def list(self, request):
        page_number = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)

        pagination_response = self.gym_component.fetch_all_gyms(page_number, page_size)

        serialized_items = [serialize_gym(gym) for gym in pagination_response.items]

        return Response({
            **pagination_response.to_dict(),
            "items": serialized_items
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        gym = self.gym_component.fetch_gym_by_id(pk)
        if not gym:
            return Response({"error": "Gym not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized_gym = serialize_gym(gym)
        return Response(serialized_gym, status=status.HTTP_200_OK)

    def create(self, request):
        validation_error = self.validator.validate_data('CREATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        gym_data = request.data
        gym = self.gym_component.add_gym(gym_data)
        serialized_gym = serialize_gym(gym)
        return Response(serialized_gym, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        validation_error = self.validator.validate_data('UPDATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        gym_data = request.data
        updated_gym = self.gym_component.modify_gym(pk, gym_data)
        if updated_gym:
            serialized_gym = serialize_gym(updated_gym)
            return Response(serialized_gym, status=status.HTTP_200_OK)
        return Response({"error": "Gym not found"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        success = self.gym_component.remove_gym(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Gym not found"}, status=status.HTTP_404_NOT_FOUND)
