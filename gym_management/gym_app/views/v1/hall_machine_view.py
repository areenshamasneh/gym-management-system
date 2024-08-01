from rest_framework import status, viewsets # type: ignore
from rest_framework.response import Response # type: ignore
from gym_app.components.hall_machine_component import HallMachineComponent
from gym_app.serializers import HallMachineSerializer

class HallMachineViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component = HallMachineComponent()

    def list(self, request, gym_id=None):
        if gym_id:
            hall_machines = self.component.fetch_hall_machines_by_gym(gym_id)
        else:
            hall_machines = self.component.fetch_all_hall_machines()
        serializer = HallMachineSerializer(hall_machines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
