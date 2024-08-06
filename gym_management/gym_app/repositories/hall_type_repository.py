from django.db import IntegrityError
from gym_app.exceptions import ResourceNotFoundException, DatabaseException
from gym_app.models import HallType


class HallTypeRepository:

    @staticmethod
    def get_all_hall_types():
        return HallType.objects.all()

    @staticmethod
    def get_hall_type_by_id(hall_type_id):
        try:
            return HallType.objects.get(pk=hall_type_id)
        except HallType.DoesNotExist:
            raise ResourceNotFoundException(f"HallType with ID {hall_type_id} not found")

    @staticmethod
    def create_hall_type(data):
        try:
            return HallType.objects.create(**data)
        except IntegrityError as e:
            raise DatabaseException(f"Error creating HallType: {e}")

    @staticmethod
    def update_hall_type(hall_type_id, data):
        try:
            hall_type = HallType.objects.get(pk=hall_type_id)

            if 'code' in data and data['code'] != hall_type.code:
                existing_hall_type = HallType.objects.filter(code=data['code']).exclude(pk=hall_type_id).first()
                if existing_hall_type:
                    raise DatabaseException("Code already exists for another hall type.")

            for key, value in data.items():
                setattr(hall_type, key, value)
            hall_type.save()

            return hall_type
        except HallType.DoesNotExist:
            raise ResourceNotFoundException(f"HallType with ID {hall_type_id} not found")
        except IntegrityError as e:
            raise DatabaseException(f"Error updating HallType: {e}")

    @staticmethod
    def delete_hall_type(hall_type_id):
        try:
            affected_rows = HallType.objects.filter(pk=hall_type_id).delete()
            if affected_rows[0] == 0:
                raise ResourceNotFoundException(f"HallType with ID {hall_type_id} not found")
        except IntegrityError as e:
            raise DatabaseException(f"Error deleting HallType: {e}")
