from rest_framework import status, viewsets
from rest_framework.response import Response
from gym_app.components.hall_machine_component import HallMachineComponent
from gym_app.serializers import HallMachineSerializer


class HallMachineViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component = HallMachineComponent()

    def list(self, request, gym_id=None):
        try:
            hall_machines = self.component.fetch_hall_machines_by_gym(gym_id)
            serializer = HallMachineSerializer(hall_machines, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
