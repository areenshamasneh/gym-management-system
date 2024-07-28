from gym_app.models import Gym


class GymRepository:
    @staticmethod
    def get_all_gyms():
        return Gym.objects.all()

    @staticmethod
    def get_gym_by_id(pk):
        return Gym.objects.get(pk=pk)

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
        gym = Gym.objects.get(pk=pk)
        gym.name = data.get("name", gym.name)
        gym.type = data.get("type", gym.type)
        gym.description = data.get("description", gym.description)
        gym.address_city = data.get("address_city", gym.address_city)
        gym.address_street = data.get("address_street", gym.address_street)
        gym.save()
        return gym

    @staticmethod
    def delete_gym(pk):
        Gym.objects.get(pk=pk).delete()
