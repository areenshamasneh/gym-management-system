from django.db import transaction
from django.shortcuts import get_object_or_404

from gym_app.models import Hall, Gym


class HallRepository:
    @staticmethod
    def get_all_halls(gym_id):
        return Hall.objects.filter(gym_id=gym_id).select_related('gym_id')

    @staticmethod
    def get_hall_by_id(gym_id, hall_id):
        return get_object_or_404(Hall.objects.select_related('gym_id'), pk=hall_id, gym_id=gym_id)

    @transaction.atomic
    def create_hall(self, gym_id, data):
        hall_type_id = data.get("hall_type_id")
        if not hall_type_id:
            raise ValueError("hall_type_id is required")

        # Fetch the gym instance
        gym_instance = get_object_or_404(Gym.objects.only('id'), pk=gym_id)
        return Hall.objects.create(
            name=data.get("name"),
            users_capacity=data.get("users_capacity"),
            hall_type_id=hall_type_id,
            gym_id=gym_instance,
        )

    @transaction.atomic
    def update_hall(self, gym_id, hall_id, data):
        hall = get_object_or_404(Hall.objects.select_related('gym_id'), pk=hall_id, gym_id=gym_id)
        for attr, value in data.items():
            if attr == "hall_type_id" and not value:
                raise ValueError("hall_type_id is required")
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
