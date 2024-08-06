from rest_framework import viewsets, status
from rest_framework.response import Response
from gym_app.components import MachineComponent
from gym_app.models import Machine
from gym_app.serializers import MachineSerializer


class MachineViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        self.component = MachineComponent()
        super().__init__(**kwargs)

    def list(self, request, gym_id=None, hall_id=None):
        try:
            machines = self.component.fetch_all_machines_in_hall(gym_id, hall_id)
            serializer = MachineSerializer([hm.machine_id for hm in machines], many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, gym_id=None, hall_id=None):
        data = request.data
        try:
            machine, created = Machine.objects.get_or_create(
                serial_number=data["serial_number"],
                defaults={
                    "type": data.get("type"),
                    "model": data.get("model"),
                    "brand": data.get("brand"),
                    "status": data.get("status"),
                    "maintenance_date": data.get("maintenance_date"),
                },
            )

            if created:
                self.component.logger.log_info(f"Machine created: {machine.serial_number}")
            else:
                self.component.logger.log_info(
                    f"Machine already exists: {machine.serial_number}"
                )

            hall_machine = self.component.add_hall_machine(
                gym_id,
                hall_id,
                {
                    "name": data.get("name"),
                    "uid": data.get("uid"),
                    "machine_id": machine.id,
                },
            )

            serializer = MachineSerializer(machine)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, gym_id=None, hall_id=None, pk=None):
        try:
            machine = self.component.fetch_machine_by_id_in_hall(gym_id, hall_id, pk)
            serializer = MachineSerializer(machine)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, gym_id=None, hall_id=None, pk=None):
        data = request.data
        try:
            machine = Machine.objects.get(pk=pk)
            serializer = MachineSerializer(machine, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                hall_machine = self.component.modify_hall_machine(gym_id, hall_id, pk, data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, gym_id=None, hall_id=None, pk=None):
        try:
            machine = Machine.objects.get(pk=pk)
            self.component.remove_hall_machine(gym_id, hall_id, pk)
            machine.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
