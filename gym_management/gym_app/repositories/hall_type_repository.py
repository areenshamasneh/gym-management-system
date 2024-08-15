from gym_app.exceptions import DatabaseException
from gym_app.models import HallType


class HallTypeRepository:

    @staticmethod
    def get_all_hall_types():
        return HallType.objects.all()

    @staticmethod
    def get_hall_type_by_id(hall_type_id):
        return HallType.objects.get(pk=hall_type_id)

    @staticmethod
    def create_hall_type(data):
        return HallType.objects.create(**data)

    @staticmethod
    def update_hall_type(hall_type_id, data):
        hall_type = HallType.objects.get(pk=hall_type_id)

        if 'code' in data and data['code'] != hall_type.code:
            existing_hall_type = HallType.objects.filter(code=data['code']).exclude(pk=hall_type_id).first()
            if existing_hall_type:
                raise DatabaseException("Code already exists for another hall type.")

        for key, value in data.items():
            setattr(hall_type, key, value)
        hall_type.save()
        return hall_type

    @staticmethod
    def delete_hall_type(hall_type_id):
        HallType.objects.filter(pk=hall_type_id).delete()
