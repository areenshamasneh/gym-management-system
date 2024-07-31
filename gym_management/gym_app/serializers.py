from rest_framework import serializers  # type: ignore
from gym_app.models import (
    Gym,
    Machine,
    HallType,
    Hall,
    Admin,
    Employee,
    Member,
    HallMachine,
)


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ["id", "name", "type", "description", "address_city", "address_street"]


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = "__all__"


class HallTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallType
        fields = "__all__"


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = "__all__"


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "address_city",
            "address_street",
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class HallMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallMachine
        fields = "__all__"
