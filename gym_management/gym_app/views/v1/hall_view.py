from rest_framework import viewsets, status  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.exceptions import NotFound  # type: ignore
from gym_app.serializers import HallSerializer
from gym_app.components import HallComponent
from django.core.exceptions import ValidationError


class HallViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        self.hall_component = HallComponent()
        super().__init__(**kwargs)

    def list(self, request, gym_id=None):
        try:
            halls = self.hall_component.fetch_all_halls(gym_id)
            serializer = HallSerializer(halls, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, gym_id=None, pk=None):
        try:
            hall = self.hall_component.fetch_hall_by_id(gym_id, pk)
            serializer = HallSerializer(hall)
            return Response(serializer.data)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, gym_id=None):
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            try:
                hall = self.hall_component.add_hall(gym_id, serializer.validated_data)
                serializer = HallSerializer(hall)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def update(self, request, gym_id=None, pk=None):
        serializer = HallSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                hall = self.hall_component.modify_hall(
                    gym_id, pk, serializer.validated_data
                )
                serializer = HallSerializer(hall)
                return Response(serializer.data)
            except NotFound as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def partial_update(self, request, gym_id=None, pk=None):
        serializer = HallSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                hall = self.hall_component.modify_hall(
                    gym_id, pk, serializer.validated_data
                )
                serializer = HallSerializer(hall)
                return Response(serializer.data)
            except NotFound as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, gym_id=None, pk=None):
        try:
            self.hall_component.remove_hall(gym_id, pk)
            return Response(
                {"message": "Hall deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
