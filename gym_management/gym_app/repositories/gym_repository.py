from gym_app.models import Gym


class GymRepository:
    def get_all_gyms(self):
        return Gym.objects.all()

    def get_gym_by_id(self, pk):
        return Gym.objects.get(pk=pk)

    def create_gym(self, data):
        return Gym.objects.create(
            name=data.get("name"),
            type=data.get("type"),
            description=data.get("description"),
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
        )

    def update_gym(self, pk, data):
        gym = Gym.objects.get(pk=pk)
        gym.name = data.get("name", gym.name)
        gym.type = data.get("type", gym.type)
        gym.description = data.get("description", gym.description)
        gym.address_city = data.get("address_city", gym.address_city)
        gym.address_street = data.get("address_street", gym.address_street)
        gym.save()
        return gym

    def delete_gym(self, pk):
        Gym.objects.get(pk=pk).delete()
