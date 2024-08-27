import importlib

from marshmallow import Schema, fields


class HallMachineSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    uid = fields.Str()
    hall = fields.Method('get_hall')
    machine = fields.Method('get_machine')

    def get_hall(self, obj):
        HallSerializer = importlib.import_module('gym_app.serializers.v1.hall_serializer').HallSerializer
        hall_data = HallSerializer().dump(obj.hall)
        return hall_data

    def get_machine(self, obj):
        MachineSerializer = importlib.import_module('gym_app.serializers.v1.machine_serializer').MachineSerializer
        machine_data = MachineSerializer().dump(obj.machine)
        return machine_data
