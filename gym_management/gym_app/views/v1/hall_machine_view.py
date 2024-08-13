from rest_framework import viewsets, status
from rest_framework.response import Response

from gym_app.components.hall_machine_component import HallMachineComponent
from gym_app.models.system_models import HallMachine
from gym_app.serializers import HallMachineSerializer
from gym_app.validators import SchemaValidator


class HallMachineViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component = HallMachineComponent()
        self.validator = SchemaValidator('gym_app.schemas.hall_machine_schemas')

    def list(self, request, gym_pk=None):
        if gym_pk:
            try:
                machines = self.component.fetch_hall_machines_by_gym(gym_pk)
                serializer = HallMachineSerializer(machines, many=True)
                return Response(serializer.data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, gym_pk=None):
        if pk:
            try:
                machine = self.component.fetch_hall_machine_by_id(pk)
                serializer = HallMachineSerializer(machine)
                return Response(serializer.data)
            except HallMachine.DoesNotExist:
                return Response({"error": "Hall machine not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
