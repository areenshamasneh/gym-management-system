from gym_app.models import Gym
from django.core.paginator import Paginator


class GymRepository:
    @staticmethod
    def get_all_gyms(page_number=1, page_size=10):
        gyms = Gym.objects.all()
        paginator = Paginator(gyms, page_size)
        return paginator.get_page(page_number)

    @staticmethod
    def get_gym_by_id(pk):
        return Gym.objects.filter(pk=pk).first()

    @staticmethod
    def create_gym(data):
        gym = Gym.objects.create(
            name=data.get("name"),
            type=data.get("type"),
            description=data.get("description"),
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
        )
        return gym

    @staticmethod
    def update_gym(pk, data):
        gym = Gym.objects.filter(pk=pk).first()
        if gym:
            Gym.objects.filter(pk=pk).update(
                name=data.get("name"),
                type=data.get("type"),
                description=data.get("description"),
                address_city=data.get("address_city"),
                address_street=data.get("address_street"),
            )
        return gym

    @staticmethod
    def delete_gym(pk):
        deleted, _ = Gym.objects.filter(pk=pk).delete()
        return deleted > 0
