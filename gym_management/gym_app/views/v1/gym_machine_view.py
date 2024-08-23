from rest_framework import viewsets, status
from rest_framework.response import Response

from gym_app.components import MachineComponent
from gym_app.exceptions import ResourceNotFoundException, DatabaseException
from gym_app.serializers import serialize_machine
from gym_app.validators import SchemaValidator


class GymMachineViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.component = MachineComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.schemas.machine_schemas')

    def list(self, request, gym_pk=None):
        try:
            machines = self.component.fetch_all_machines_in_gym(gym_pk)
            serialized_machines = [serialize_machine(hm.machine) for hm in machines]
            return Response(serialized_machines, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error in list: {str(e)}")
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, gym_pk=None, pk=None):
        try:
            machine = self.component.fetch_machine_by_id_in_gym(gym_pk, pk)
            if not machine:
                raise ResourceNotFoundException(f"Machine with ID {pk} not found in gym {gym_pk}.")

            serialized_machine = serialize_machine(machine)
            return Response(serialized_machine, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error in retrieve: {str(e)}")
            return Response({'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
