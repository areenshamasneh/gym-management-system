from django.shortcuts import get_object_or_404

from gym_app.models import HallType


class HallTypeRepository:

    def get_all_hall_types(self):
        return HallType.objects.all()

    def get_hall_type_by_id(self, hall_type_id):
        return get_object_or_404(HallType, pk=hall_type_id)

    def create_hall_type(self, data):
        return HallType.objects.create(**data)

    def update_hall_type(self, hall_type_id, data):
        hall_type = get_object_or_404(HallType, pk=hall_type_id)
        for attr, value in data.items():
            setattr(hall_type, attr, value)
        hall_type.save()
        return hall_type

    def delete_hall_type(self, hall_type_id):
        hall_type = get_object_or_404(HallType, pk=hall_type_id)
        hall_type.delete()
