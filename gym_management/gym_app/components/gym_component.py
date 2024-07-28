from gym_app.repositories.gym_repository import GymRepository


class GymComponent:

    def fetch_all_gyms():
        return GymRepository.get_all_gyms()

    def fetch_gym_by_id(pk):
        return GymRepository.get_gym_by_id(pk)

    def add_gym(data):
        return GymRepository.create_gym(data)

    def modify_gym(pk, data):
        return GymRepository.update_gym(pk, data)

    def remove_gym(pk):
        return GymRepository.delete_gym(pk)
