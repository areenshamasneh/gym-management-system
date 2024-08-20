from gym_app.models import HallMachine, Hall


class HallMachineRepository:
    @staticmethod
    def get_hall_machines_by_gym(gym_id):
        halls = Hall.objects.filter(gym_id=gym_id).select_related('gym')
        hall_ids = halls.values_list("id", flat=True)
        return HallMachine.objects.filter(hall_id__in=hall_ids).select_related('hall__gym', 'hall__hall_type','machine')

    @staticmethod
    def get_hall_machines_by_hall(hall_id):
        return HallMachine.objects.filter(hall_id=hall_id)
