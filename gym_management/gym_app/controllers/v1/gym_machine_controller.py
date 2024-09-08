from rest_framework import viewsets, status  # type: ignore
from rest_framework.response import Response  # type: ignore

from gym_app.components import MachineComponent
from gym_app.serializers import MachineSchema
from gym_app.validators import SchemaValidator


class GymMachineController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component = MachineComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.machine_schemas')
        self.schema = MachineSchema()

    def list(self, request, gym_pk=None):
        machines = self.component.fetch_all_machines_in_gym(gym_pk)
        machine_objects = [hm.machine for hm in machines]
        serialized_machines = self.schema.dump(machine_objects, many=True)
        return Response(serialized_machines, status=status.HTTP_200_OK)

    def retrieve(self, request, gym_pk=None, pk=None):
        machine = self.component.fetch_machine_by_id_in_gym(gym_pk, pk)
        serialized_machine = self.schema.dump(machine)
        return Response(serialized_machine, status=status.HTTP_200_OK)
