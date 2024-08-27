from marshmallow import Schema, fields


class MachineSerializer(Schema):
    id = fields.Int()
    serial_number = fields.Str()
    type = fields.Str()
    model = fields.Str()
    brand = fields.Str()
    status = fields.Str()
    maintenance_date = fields.Date(format='iso')
