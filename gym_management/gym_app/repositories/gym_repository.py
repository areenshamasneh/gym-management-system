from django.core.paginator import Paginator

from gym_app.models import Gym

from django.core.paginator import Paginator
from gym_app.models import Gym
from gym_app.utils import PaginationResponse


class GymRepository:
    @staticmethod
    def get_all_gyms(page_number=1, page_size=10):
        gyms = Gym.objects.all()
        paginator = Paginator(gyms, page_size)
        paginated_gyms = paginator.get_page(page_number)

        return PaginationResponse(
            items=list(paginated_gyms),
            total_items=paginator.count,
            total_pages=paginator.num_pages,
            current_page=paginated_gyms.number,
            page_size=page_size
        )

    @staticmethod
    def get_gym_by_id(pk):
        return Gym.objects.filter(pk=pk).first()

    @staticmethod
    def create_gym(data):
        return Gym.objects.create(
            name=data.get("name"),
            type=data.get("type"),
            description=data.get("description"),
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
        )

    @staticmethod
    def update_gym(pk, data):
        gym = Gym.objects.filter(pk=pk).first()
        if gym:
            fields_to_update = ['name', 'type', 'description', 'address_city', 'address_street']
            for field in fields_to_update:
                if field in data:
                    setattr(gym, field, data[field])

            gym.save()
            return gym
        return None

    @staticmethod
    def delete_gym(pk):
        deleted, _ = Gym.objects.filter(pk=pk).delete()
        return deleted > 0
