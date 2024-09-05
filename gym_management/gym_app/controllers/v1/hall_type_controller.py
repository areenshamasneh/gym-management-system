from rest_framework import viewsets, status
from rest_framework.response import Response

from gym_app.components import HallTypeComponent
from gym_app.serializers import HallTypeSerializer


class HallTypeController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component = HallTypeComponent()
        self.schema = HallTypeSerializer()

    def list(self, request):
        hall_types = self.component.fetch_all_hall_types()
        serialized_data = self.schema.dump(hall_types, many=True)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        hall_type = self.component.fetch_hall_type_by_id(pk)
        serialized_data = self.schema.dump(hall_type)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def create(self, request):
        data = self.schema.load(request.data)
        hall_type = self.component.add_hall_type(data)
        serialized_data = self.schema.dump(hall_type)
        return Response(serialized_data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = self.schema.load(request.data)
        hall_type = self.component.modify_hall_type(pk, data)
        serialized_data = self.schema.dump(hall_type)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        self.component.remove_hall_type(pk)
        return Response({"message": "Hall Type deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
