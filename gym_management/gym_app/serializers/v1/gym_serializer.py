from marshmallow import Schema, fields


class GymSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    description = fields.Str()
    address_city = fields.Str()
    address_street = fields.Str()
