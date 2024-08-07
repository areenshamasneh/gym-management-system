from rest_framework import viewsets, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response

from gym_app.components import HallComponent
from gym_app.models import Gym
from gym_app.serializers import HallSerializer
from gym_app.validators import SchemaValidator


class HallViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        self.hall_component = HallComponent()
        self.validator = SchemaValidator('gym_app/schemas')
        super().__init__(**kwargs)

    @staticmethod
    def get_gym(gym_id):
        try:
            return Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            raise NotFound(f"Gym with ID {gym_id} does not exist")

    def list(self, request, gym_pk=None):
        if gym_pk is None:
            return Response({"detail": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        self.get_gym(gym_pk)

        try:
            halls = self.hall_component.fetch_all_halls(gym_pk)
            serializer = HallSerializer(halls, many=True)
            return Response(serializer.data)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, gym_pk=None, pk=None):
        self.get_gym(gym_pk)

        try:
            hall = self.hall_component.fetch_hall_by_id(gym_pk, pk)
            serializer = HallSerializer(hall)
            return Response(serializer.data)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, gym_pk=None):
        self.get_gym(gym_pk)

        request.data['gym_id'] = gym_pk
        validation_error = self.validator.validate_data('hall_schema.json', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            try:
                hall = self.hall_component.add_hall(gym_pk, serializer.validated_data)
                serializer = HallSerializer(hall)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({"errors": "An unexpected error occurred."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, gym_pk=None, pk=None):
        self.get_gym(gym_pk)

        request.data['gym_id'] = gym_pk
        validation_error = self.validator.validate_data('hall_schema.json', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HallSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            try:
                hall = self.hall_component.modify_hall(gym_pk, pk, serializer.validated_data)
                serializer = HallSerializer(hall)
                return Response(serializer.data)
            except NotFound as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except ValidationError as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({"errors": "An unexpected error occurred."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, gym_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, pk=pk)

    def destroy(self, request, gym_pk=None, pk=None):
        self.get_gym(gym_pk)

        try:
            hall = self.hall_component.fetch_hall_by_id(gym_pk, pk)
            if hall is None:
                return Response({"detail": "Hall not found."}, status=status.HTTP_404_NOT_FOUND)

            self.hall_component.remove_hall(gym_pk, pk)
            return Response({"message": "Hall deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except NotFound as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
