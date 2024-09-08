from rest_framework import viewsets, status  # type: ignore
from rest_framework.response import Response  # type: ignore

from gym_app.components import MachineComponent
from gym_app.exceptions import ResourceNotFoundException
from gym_app.serializers import MachineSchema
from gym_app.validators import SchemaValidator


class MachineController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component = MachineComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.machine_schemas')
        self.schema = MachineSchema()

    def list(self, request, gym_pk=None, hall_pk=None):
        machines = self.component.fetch_all_machines_in_hall(gym_pk, hall_pk)
        serialized_data = self.schema.dump(machines, many=True)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def retrieve(self, request, gym_pk=None, hall_pk=None, pk=None):
        machine = self.component.fetch_machine_by_id_in_hall(gym_pk, hall_pk, pk)
        serialized_data = self.schema.dump(machine)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def create(self, request, gym_pk=None, hall_pk=None):
        validation_error = self.validator.validate_data('CREATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        try:
            machine_data = {
                "serial_number": data["serial_number"],
                "type": data.get("type"),
                "model": data.get("model"),
                "brand": data.get("brand"),
                "status": data.get("status"),
                "maintenance_date": data.get("maintenance_date"),
            }

            hall_machine = self.component.add_machine_and_hall_machine(
                gym_pk,
                hall_pk,
                machine_data,
            )
            serialized_data = self.schema.dump(hall_machine)
            return Response(serialized_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, gym_pk=None, hall_pk=None, pk=None):
        try:
            machine = self.component.fetch_machine_by_id_in_hall(gym_pk, hall_pk, pk)
            serialized_data = self.schema.dump(machine)
            return Response(serialized_data, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, gym_pk=None, hall_pk=None, pk=None):
        validation_error = self.validator.validate_data('UPDATE_SCHEMA', request.data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        machine = self.component.fetch_machine_by_id_in_hall(gym_pk, hall_pk, pk)
        if not machine:
            raise ResourceNotFoundException(f"Machine with ID {pk} not found.")

        for attr, value in data.items():
            setattr(machine, attr, value)
        self.component.modify_machine_and_hall_machine(gym_pk, hall_pk, pk, data)
        serialized_data = self.schema.dump(machine)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def partial_update(self, request, gym_pk=None, hall_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, hall_pk=hall_pk, pk=pk)

    def destroy(self, request, gym_pk=None, hall_pk=None, pk=None):
        self.component.remove_hall_machine(gym_pk, hall_pk, pk)
        return Response({"message": "Machine deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
