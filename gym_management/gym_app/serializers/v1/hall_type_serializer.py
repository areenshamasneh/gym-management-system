from marshmallow import Schema, fields, pre_load


class HallTypeSerializer(Schema):
    id = fields.Int()
    name = fields.Str()
    code = fields.Str()
    type_description = fields.Str()

    @pre_load
    def process_input(self, data, **kwargs):
        if 'code' in data:
            data['code'] = data['code'].upper()
        if 'name' in data:
            data['name'] = data['name'].capitalize()
        return data
