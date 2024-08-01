from gym_app.models import HallMachine, Hall


class HallMachineRepository:
    def get_hall_machines_by_gym(self, gym_id):
        halls = Hall.objects.filter(gym_id=gym_id)
        if not halls.exists():
            raise ValueError("No halls found for the given gym ID")

        hall_machines = []
        for hall in halls:
            hall_machines.extend(self.get_hall_machines_by_hall(hall.id))

        return hall_machines

    def get_hall_machines_by_hall(self, hall_id):
        return HallMachine.objects.filter(hall_id=hall_id)
