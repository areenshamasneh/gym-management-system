from rest_framework import status  # type: ignore
from rest_framework import viewsets  # type: ignore
from rest_framework.response import Response  # type: ignore

from gym_app.components import GymComponent
from gym_app.serializers import GymSerializer


class GymViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gym_component = GymComponent()

    def list(self, request):
        gyms = self.gym_component.fetch_all_gyms()
        serializer = GymSerializer(gyms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        gym = self.gym_component.fetch_gym_by_id(pk)
        serializer = GymSerializer(gym)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = GymSerializer(data=request.data)
        if serializer.is_valid():
            self.gym_component.add_gym(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        serializer = GymSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            self.gym_component.modify_gym(pk, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        self.gym_component.remove_gym(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
