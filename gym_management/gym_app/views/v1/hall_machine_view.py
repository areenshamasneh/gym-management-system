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
        self.validator = SchemaValidator('gym_app/schemas')

    def list(self, request, gym_pk=None):
        if gym_pk is not None:
            try:
                machines = self.component.fetch_hall_machines_by_gym(gym_pk)
                serializer = HallMachineSerializer(machines, many=True)
                return Response(serializer.data)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Gym ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None, gym_pk=None):
        if pk is not None:
            try:
                machine = self.component.fetch_hall_machine_by_id(pk)
                serializer = HallMachineSerializer(machine)
                return Response(serializer.data)
            except HallMachine.DoesNotExist:
                return Response(
                    {"error": "Hall machine not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, gym_pk=None):
        validation_error = self.validator.validate_data('hall_machine_schema.json', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        try:
            hall_machine, created = HallMachine.objects.get_or_create(
                hall_id=data["hall_id"],
                machine_id=data["machine_id"],
                defaults={
                    "name": data.get("name"),
                    "uid": data["uid"]
                },
            )

            serializer = HallMachineSerializer(hall_machine)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        validation_error = self.validator.validate_data('hall_machine_schema.json', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        try:
            hall_machine = HallMachine.objects.get(pk=pk)
            serializer = HallMachineSerializer(hall_machine, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except HallMachine.DoesNotExist:
            return Response({"error": "Hall machine not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, pk=None):
        return self.update(request, pk=pk)

    @staticmethod
    def destroy(request, pk=None):
        try:
            hall_machine = HallMachine.objects.get(pk=pk)
            hall_machine.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HallMachine.DoesNotExist:
            return Response({"error": "Hall machine not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
