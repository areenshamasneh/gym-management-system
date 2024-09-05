import importlib
from datetime import datetime, date

from marshmallow import Schema, fields, pre_load, post_dump, ValidationError


class MemberSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    gym = fields.Method('get_gym')
    phone_number = fields.Str()
    birth_date = fields.Date(format='iso')

    @staticmethod
    def get_gym(obj):
        GymSerializer = importlib.import_module('gym_app.serializers.v1.gym_serializer').GymSerializer
        return GymSerializer().dump(obj.gym)

    @pre_load
    def process_input(self, data, **kwargs):
        if 'birth_date' in data:
            if isinstance(data['birth_date'], str):
                try:
                    data['birth_date'] = datetime.fromisoformat(data['birth_date']).date()
                except ValueError:
                    raise ValidationError("Invalid date format for birth_date")
        return data

    @post_dump
    def serialize_birth_date(self, data, **kwargs):
        if 'birth_date' in data and isinstance(data['birth_date'], date):
            data['birth_date'] = data['birth_date'].isoformat()
        return data
