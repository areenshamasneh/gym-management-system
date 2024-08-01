from gym_app.models.system_models import Hall, HallMachine


class HallMachineRepository:
    def get_hall_machines_by_gym(self, gym_id):
        halls = Hall.objects.filter(gym_id=gym_id)
        if not halls.exists():
            raise ValueError("No halls found for the given gym ID")

        hall_ids = halls.values_list("id", flat=True)

        return HallMachine.objects.filter(hall_id__in=hall_ids)
