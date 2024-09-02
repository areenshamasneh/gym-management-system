import importlib

from marshmallow import Schema, fields


class EmployeeSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    gym = fields.Method('get_gym')

    @staticmethod
    def get_gym(obj):
        GymSerializer = importlib.import_module('gym_app.serializers.v1.gym_serializer').GymSerializer
        return GymSerializer().dump(obj.gym)

    manager = fields.Nested('self', exclude=('manager',))
    address_city = fields.Str()
    address_street = fields.Str()
    phone_number = fields.Str()
    email = fields.Str()
    positions = fields.List(fields.Str())
