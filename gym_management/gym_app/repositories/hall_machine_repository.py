from gym_app.exceptions import ResourceNotFoundException
from gym_app.models import HallMachine, Hall


class HallMachineRepository:
    @staticmethod
    def get_hall_machines_by_gym(gym_id):
        halls = Hall.objects.filter(gym_id=gym_id)
        if not halls.exists():
            raise ResourceNotFoundException("No halls found for the given gym ID")

        hall_ids = halls.values_list("id", flat=True)
        return HallMachine.objects.filter(hall_id__in=hall_ids)

    @staticmethod
    def get_hall_machines_by_hall(hall_id):
        hall_machines = HallMachine.objects.filter(hall_id=hall_id)
        if not hall_machines.exists():
            raise ResourceNotFoundException(f"No hall machines found for hall ID {hall_id}")
        return hall_machines

