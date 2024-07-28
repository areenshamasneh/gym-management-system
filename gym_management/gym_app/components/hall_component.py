from gym_app.repositories.hall_repository import HallRepository


class HallComponent:

    def fetch_all_halls(gym_id):
        return HallRepository.get_all_halls(gym_id)

    def fetch_hall_by_id(gym_id, hall_id):
        return HallRepository.get_hall_by_id(gym_id, hall_id)

    def add_hall(gym_id, data):
        return HallRepository.create_hall(gym_id, data)

    def modify_hall(gym_id, hall_id, data):
        return HallRepository.update_hall(gym_id, hall_id, data)

    def remove_hall(gym_id, hall_id):
        return HallRepository.delete_hall(gym_id, hall_id)
