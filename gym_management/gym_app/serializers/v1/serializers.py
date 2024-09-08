from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from gym_app.models.models_sqlalchemy import Gym, Admin, Machine, Hall, HallType, Member, HallMachine, Employee

class GymSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Gym
        include_relationships = False
        load_instance = True

class AdminSchema(SQLAlchemyAutoSchema):
    gym = Nested(GymSchema)

    class Meta:
        model = Admin
        include_relationships = False
        load_instance = True

class MachineSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Machine
        include_relationships = False
        load_instance = True

class HallTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = HallType
        include_relationships = False
        load_instance = True

class HallSchema(SQLAlchemyAutoSchema):
    hall_type = Nested(HallTypeSchema)
    gym = Nested(GymSchema)

    class Meta:
        model = Hall
        include_relationships = False
        load_instance = True

class MemberSchema(SQLAlchemyAutoSchema):
    gym = Nested(GymSchema) 

    class Meta:
        model = Member
        include_relationships = False
        load_instance = True

class HallMachineSchema(SQLAlchemyAutoSchema):
    hall = Nested(HallSchema) 
    machine = Nested(MachineSchema)

    class Meta:
        model = HallMachine
        include_relationships = False
        load_instance = True

class EmployeeSchema(SQLAlchemyAutoSchema):
    gym = Nested(GymSchema)
    manager = Nested('EmployeeSchema', exclude=('manager',))

    class Meta:
        model = Employee
        include_relationships = False
        load_instance = True
