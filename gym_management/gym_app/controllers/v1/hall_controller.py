from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from gym_app.components import HallComponent, HallMachineComponent
from gym_app.serializers import HallSerializer, HallMachineSerializer
from gym_app.validators import SchemaValidator


class HallController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hall_component = HallComponent()
        self.hall_machine_component = HallMachineComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.hall_schemas')
        self.hall_schema = HallSerializer()
        self.hall_machine_schema = HallMachineSerializer()

    def list(self, request, gym_pk=None):
        if gym_pk is None:
            return Response({"detail": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        halls = self.hall_component.fetch_all_halls(gym_pk)
        serialized_data = self.hall_schema.dump(halls, many=True)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def retrieve(self, request, gym_pk=None, pk=None):
        hall = self.hall_component.fetch_hall_by_id(gym_pk, pk)
        serialized_data = self.hall_schema.dump(hall)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def create(self, request, gym_pk=None):
        validation_error = self.validator.validate_data('CREATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['gym'] = gym_pk
        hall = self.hall_component.add_hall(gym_pk, data)
        serialized_data = self.hall_schema.dump(hall)
        return Response(serialized_data, status=status.HTTP_201_CREATED)

    def update(self, request, gym_pk=None, pk=None):
        validation_error = self.validator.validate_data('UPDATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        hall = self.hall_component.modify_hall(gym_pk, pk, request.data)
        serialized_data = self.hall_schema.dump(hall)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def partial_update(self, request, gym_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, pk=pk)

    def destroy(self, request, gym_pk=None, pk=None):
        hall = self.hall_component.fetch_hall_by_id(gym_pk, pk)
        if hall is None:
            return Response({"detail": "Hall not found."}, status=status.HTTP_404_NOT_FOUND)

        self.hall_component.remove_hall(gym_pk, pk)
        return Response({"message": "Hall deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'], detail=False, url_path='machines', url_name='all-hall-machines')
    def list_all_hall_machines(self, request, gym_pk=None):
        if gym_pk:
            machines = self.hall_machine_component.fetch_hall_machines_by_gym(gym_pk)
            serialized_data = self.hall_machine_schema.dump(machines, many=True)
            return Response(serialized_data)
        return Response({"error": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST)
