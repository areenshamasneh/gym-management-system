from gym_app.repositories.hall_repository import HallRepository


class HallComponent:
    @staticmethod
    def fetch_all_halls():
        return HallRepository.get_all_halls()

    @staticmethod
    def fetch_hall_by_id(hall_id):
        return HallRepository.get_hall_by_id(hall_id)

    @staticmethod
    def add_hall(data):
        return HallRepository.create_hall(data)

    @staticmethod
    def modify_hall(hall_id, data):
        return HallRepository.update_hall(hall_id, data)

    @staticmethod
    def remove_hall(hall_id):
        return HallRepository.delete_hall(hall_id)
