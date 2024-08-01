from gym_app.models import HallMachine, Hall


class HallMachineRepository:
    def get_hall_machines_by_gym(self, gym_id):
        halls = Hall.objects.filter(gym_id=gym_id)
        if not halls.exists():
            raise ValueError("No halls found for the given gym ID")

        hall_ids = halls.values_list("id", flat=True)
        return HallMachine.objects.filter(hall_id__in=hall_ids)

    def get_hall_machines_by_hall(self, hall_id):
        return HallMachine.objects.filter(hall_id=hall_id)

    def get_hall_machine_by_id(self, machine_id):
        return HallMachine.objects.get(id=machine_id)
