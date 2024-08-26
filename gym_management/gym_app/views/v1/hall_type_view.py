from rest_framework import viewsets, status
from rest_framework.response import Response

from gym_app.components import HallTypeComponent
from gym_app.exceptions import ResourceNotFoundException, InvalidInputException
from gym_app.serializers import HallTypeSchema


class HallTypeViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component = HallTypeComponent()
        self.schema = HallTypeSchema()

    def list(self, request):
        try:
            hall_types = self.component.fetch_all_hall_types()
            serialized_data = self.schema.dump(hall_types, many=True)
            return Response(serialized_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            hall_type = self.component.fetch_hall_type_by_id(pk)
            if hall_type is None:
                raise ResourceNotFoundException(f"HallType with ID {pk} not found.")
            serialized_data = self.schema.dump(hall_type)
            return Response(serialized_data, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        data = request.data.copy()
        data['code'] = data.get('code', '').upper()
        data['name'] = data.get('name', '').capitalize()

        try:
            hall_type = self.component.add_hall_type(data)
            serialized_data = self.schema.dump(hall_type)
            return Response(serialized_data, status=status.HTTP_201_CREATED)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        data = request.data.copy()
        data['code'] = data.get('code', '').upper()
        data['name'] = data.get('name', '').capitalize()

        try:
            hall_type = self.component.modify_hall_type(pk, data)
            serialized_data = self.schema.dump(hall_type)
            return Response(serialized_data, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidInputException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        try:
            self.component.remove_hall_type(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
