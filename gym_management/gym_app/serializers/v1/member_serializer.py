import importlib

from marshmallow import Schema, fields


class MemberSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    gym = fields.Method('get_gym')

    @staticmethod
    def get_gym(obj):
        GymSerializer = importlib.import_module('gym_app.serializers.v1.gym_serializer').GymSerializer
        return GymSerializer().dump(obj.gym)

    phone_number = fields.Str()
    birth_date = fields.DateTime(format='iso')
