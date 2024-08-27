import importlib

from marshmallow import Schema, fields


class HallSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    users_capacity = fields.Int()
    hall_type = fields.Method('get_hall_type')
    gym = fields.Method('get_gym')

    @staticmethod
    def get_hall_type(obj):
        HallTypeSerializer = importlib.import_module('gym_app.serializers.v1.hall_type_serializer').HallTypeSerializer
        return HallTypeSerializer().dump(obj.hall_type)

    def get_gym(self, obj):
        GymSerializer = importlib.import_module('gym_app.serializers.v1.gym_serializer').GymSerializer
        return GymSerializer().dump(obj.gym)
