from rest_framework import status, viewsets
from rest_framework.response import Response

from gym_app.components import GymComponent
from gym_app.serializers import GymSerializer
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

        serializer = GymSerializer(pagination_response.items, many=True)

        return Response({
            **pagination_response.to_dict(),
            "items": serializer.data
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        gym = self.gym_component.fetch_gym_by_id(pk)
        if not gym:
            return Response({"error": "Gym not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = GymSerializer(gym)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        validation_error = self.validator.validate_data('CREATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GymSerializer(data=request.data)
        if serializer.is_valid():
            gym = self.gym_component.add_gym(serializer.validated_data)
            return Response(GymSerializer(gym).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        validation_error = self.validator.validate_data('UPDATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GymSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            updated_gym = self.gym_component.modify_gym(pk, serializer.validated_data)
            if updated_gym:
                return Response(GymSerializer(updated_gym).data, status=status.HTTP_200_OK)
            return Response({"error": "Gym not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        success = self.gym_component.remove_gym(pk)
        if success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Gym not found"}, status=status.HTTP_404_NOT_FOUND)
