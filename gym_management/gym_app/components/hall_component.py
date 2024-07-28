from gym_app.repositories.hall_repository import HallRepository


class HallComponent:

    def fetch_all_halls():
        return HallRepository.get_all_halls()

    def fetch_hall_by_id(hall_id):
        return HallRepository.get_hall_by_id(hall_id)

    def add_hall(data):
        return HallRepository.create_hall(data)

    def modify_hall(hall_id, data):
        return HallRepository.update_hall(hall_id, data)

    def remove_hall(hall_id):
        return HallRepository.delete_hall(hall_id)
