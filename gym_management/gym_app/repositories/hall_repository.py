from gym_app.models import Hall, Gym
from django.shortcuts import get_object_or_404


class HallRepository:
    def get_all_halls(self, gym_id):
        return Hall.objects.filter(gym_id=gym_id)

    def get_hall_by_id(self, gym_id, hall_id):
        return get_object_or_404(Hall, pk=hall_id, gym_id=gym_id)

    def create_hall(self, gym_id, data):
        hall_type_id = data.get("hall_type_id")
        if not hall_type_id:
            raise ValueError("hall_type_id is required")

        gym_instance = get_object_or_404(Gym, pk=gym_id)
        return Hall.objects.create(
            name=data.get("name"),
            users_capacity=data.get("users_capacity"),
            hall_type_id=hall_type_id,
            gym_id=gym_instance,
        )

    def update_hall(self, gym_id, hall_id, data):
        hall = get_object_or_404(Hall, pk=hall_id, gym_id=gym_id)
        for attr, value in data.items():
            if attr == "hall_type_id" and not value:
                raise ValueError("hall_type_id is required")
            setattr(hall, attr, value)
        hall.save()
        return hall

    def delete_hall(self, gym_id, hall_id):
        hall = get_object_or_404(Hall, pk=hall_id, gym_id=gym_id)
        hall.delete()
