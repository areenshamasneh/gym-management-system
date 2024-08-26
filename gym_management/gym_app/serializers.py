from marshmallow import Schema, fields


class GymSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    description = fields.Str()
    address_city = fields.Str()
    address_street = fields.Str()


class HallTypeSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    code = fields.Str()
    type_description = fields.Str()


class MachineSchema(Schema):
    id = fields.Int()
    serial_number = fields.Str()
    type = fields.Str()
    model = fields.Str()
    brand = fields.Str()
    status = fields.Str()
    maintenance_date = fields.Date(format='iso')


class HallSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    users_capacity = fields.Int()
    hall_type = fields.Nested(HallTypeSchema())
    gym = fields.Nested(GymSchema())


class HallMachineSchema(Schema):
    id = fields.Int()
    hall = fields.Nested(HallSchema())
    machine = fields.Nested(MachineSchema())
    name = fields.Str()
    uid = fields.Str()


class AdminSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    phone_number = fields.Str()
    email = fields.Str()
    gym = fields.Nested(GymSchema())
    address_city = fields.Str()
    address_street = fields.Str()


class EmployeeSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    gym = fields.Nested(GymSchema())
    manager = fields.Nested('self', exclude=('manager',))
    address_city = fields.Str()
    address_street = fields.Str()
    phone_number = fields.Str()
    email = fields.Str()
    positions = fields.List(fields.Str())


class MemberSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    gym = fields.Nested(GymSchema())
    phone_number = fields.Str()
    birth_date = fields.DateTime(format='iso')
