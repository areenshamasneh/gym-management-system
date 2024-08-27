from marshmallow import Schema, fields


class HallTypeSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    code = fields.Str()
    type_description = fields.Str()
