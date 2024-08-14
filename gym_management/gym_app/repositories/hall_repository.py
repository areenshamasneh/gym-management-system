from django.db import transaction
from django.shortcuts import get_object_or_404

from gym_app.models import Hall, Gym


class HallRepository:
    @staticmethod
    def get_all_halls(gym_id):
        return Hall.objects.filter(gym_id=gym_id).select_related('gym', 'hall_type')

    @staticmethod
    def get_hall_by_id(gym_id, hall_id):
        return Hall.objects.get(id=hall_id, gym_id=gym_id)


    @transaction.atomic
    def create_hall(self, gym_id, data):
        hall_type_instance = data.get("hall_type")
        gym_instance = get_object_or_404(Gym, pk=gym_id)

        return Hall.objects.create(
            name=data.get("name"),
            users_capacity=data.get("users_capacity"),
            hall_type=hall_type_instance,
            gym=gym_instance,
        )

    @transaction.atomic
    def update_hall(self, gym_id, hall_id, data):
        hall = get_object_or_404(Hall, pk=hall_id, gym_id=gym_id)
        if 'hall_type' in data:
            hall_type_instance = data.get("hall_type")
            hall.hall_type = hall_type_instance
        if 'gym' in data:
            gym_instance = get_object_or_404(Gym, pk=data['gym'])
            hall.gym = gym_instance
        for attr, value in data.items():
            if hasattr(hall, attr):
                setattr(hall, attr, value)

        hall.save()
        return hall

    @staticmethod
    def delete_hall(gym_id, hall_id):
        try:
            hall = Hall.objects.get(pk=hall_id, gym_id=gym_id)
            hall.delete()
            return True
        except Hall.DoesNotExist:
            return False
