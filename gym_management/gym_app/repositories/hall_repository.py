from gym_app.models import Hall, HallType, Gym
from django.shortcuts import get_object_or_404


class HallRepository:

    def get_all_halls():
        return Hall.objects.all()

    def get_hall_by_id(hall_id):
        return get_object_or_404(Hall, pk=hall_id)

    def create_hall(data):
        hall_type = get_object_or_404(HallType, pk=data.get("hall_type_id"))
        gym_instance = get_object_or_404(Gym, pk=data.get("gym_id"))
        return Hall.objects.create(
            name=data.get("name"),
            users_capacity=data.get("users_capacity"),
            hall_type=hall_type,
            gym=gym_instance,
        )

    def update_hall(hall_id, data):
        hall = get_object_or_404(Hall, pk=hall_id)
        for attr, value in data.items():
            if attr == "hall_type_id":
                hall_type = get_object_or_404(HallType, pk=value)
                setattr(hall, "hall_type", hall_type)
            elif attr == "gym_id":
                gym_instance = get_object_or_404(Gym, pk=value)
                setattr(hall, "gym", gym_instance)
            else:
                setattr(hall, attr, value)
        hall.save()
        return hall

    def delete_hall(hall_id):
        hall = get_object_or_404(Hall, pk=hall_id)
        hall.delete()
