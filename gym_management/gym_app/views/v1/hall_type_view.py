from rest_framework import viewsets, status
from rest_framework.response import Response

from gym_app.components import HallTypeComponent
from gym_app.models.system_models import HallType
from gym_app.serializers import HallTypeSerializer
from gym_app.validators import SchemaValidator


class HallTypeViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component = HallTypeComponent()
        self.validator = SchemaValidator('gym_app/schemas')

    def list(self, request):
        hall_types = self.component.fetch_all_hall_types()
        serializer = HallTypeSerializer(hall_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            hall_type = self.component.fetch_hall_type_by_id(pk)
            serializer = HallTypeSerializer(hall_type)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except HallType.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        request.data['code'] = request.data.get('code', '').upper()
        validation_error = self.validator.validate_data('hall_type_schema.json', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HallTypeSerializer(data=request.data)
        if serializer.is_valid():
            self.component.add_hall_type(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        request.data['code'] = request.data.get('code', '').upper()
        validation_error = self.validator.validate_data('hall_type_schema.json', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HallTypeSerializer(data=request.data)
        if serializer.is_valid():
            self.component.modify_hall_type(pk, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        self.component.remove_hall_type(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
