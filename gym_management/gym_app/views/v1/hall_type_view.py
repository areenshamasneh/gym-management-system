from pydantic import ValidationError as PydanticValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response

from gym_app.components import HallTypeComponent
from gym_app.models import HallType
from gym_app.models import HallTypeModel
from gym_app.serializers import HallTypeSerializer


class HallTypeViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component = HallTypeComponent()

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

        try:
            validated_data = HallTypeModel(**request.data).dict()
        except PydanticValidationError as e:
            error_details = {
                "non_field_errors": [
                    {"type": "value_error", "loc": [k], "msg": f"Value error, Invalid value for {k}: {v}", "input": v}
                    for e_detail in e.errors()
                    for k, v in e_detail.items()
                ]
            }
            return Response(error_details, status=status.HTTP_400_BAD_REQUEST)

        validated_data['name'] = validated_data['name'].capitalize()
        validated_data['code'] = validated_data['code'].upper()

        serializer = HallTypeSerializer(data=validated_data)
        if serializer.is_valid():
            self.component.add_hall_type(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        request.data['code'] = request.data.get('code', '').upper()

        try:
            validated_data = HallTypeModel(**request.data).dict()
        except PydanticValidationError as e:
            return Response({"error": e.errors()}, status=status.HTTP_400_BAD_REQUEST)

        validated_data['name'] = validated_data['name'].capitalize()
        validated_data['code'] = validated_data['code'].upper()

        serializer = HallTypeSerializer(data=validated_data, partial=True)
        if serializer.is_valid():
            self.component.modify_hall_type(pk, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        self.component.remove_hall_type(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
