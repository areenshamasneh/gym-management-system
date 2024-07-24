from gym_app.models import HallType
from django.shortcuts import get_object_or_404


class HallTypeRepository:
    @staticmethod
    def get_all_hall_types():
        return HallType.objects.all()

    @staticmethod
    def get_hall_type_by_id(hall_type_id):
        return get_object_or_404(HallType, pk=hall_type_id)

    @staticmethod
    def create_hall_type(data):
        return HallType.objects.create(**data)

    @staticmethod
    def update_hall_type(hall_type_id, data):
        hall_type = get_object_or_404(HallType, pk=hall_type_id)
        for attr, value in data.items():
            setattr(hall_type, attr, value)
        hall_type.save()
        return hall_type

    @staticmethod
    def delete_hall_type(hall_type_id):
        hall_type = get_object_or_404(HallType, pk=hall_type_id)
        hall_type.delete()
