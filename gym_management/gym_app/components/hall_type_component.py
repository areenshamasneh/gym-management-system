from gym_app.repositories.hall_type_repository import HallTypeRepository


class HallTypeComponent:

    def fetch_all_hall_types():
        return HallTypeRepository.get_all_hall_types()

    def fetch_hall_type_by_id(hall_type_id):
        return HallTypeRepository.get_hall_type_by_id(hall_type_id)

    def add_hall_type(data):
        return HallTypeRepository.create_hall_type(data)

    def modify_hall_type(hall_type_id, data):
        return HallTypeRepository.update_hall_type(hall_type_id, data)

    def remove_hall_type(hall_type_id):
        HallTypeRepository.delete_hall_type(hall_type_id)
