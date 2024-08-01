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


class HallTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallType
        fields = "__all__"


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = [
            "id",
            "serial_number",
            "type",
            "model",
            "brand",
            "status",
            "maintenance_date",
        ]


class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = ["id", "name", "users_capacity", "hall_type_id", "gym_id"]


class HallMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallMachine
        fields = ["id", "hall_id", "machine_id", "name", "uid"]


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
        fields = [
            "id",
            "name",
            "gym_id",
            "manager_id",
            "address_city",
            "address_street",
            "phone_number",
            "email",
            "positions",
        ]

    def validate_email(self, value):
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_positions(self, value):
        positions_list = [pos.strip() for pos in value.split(",") if pos.strip()]
        valid_positions = {"cleaner", "trainer", "system_worker"}
        if not set(positions_list).issubset(valid_positions):
            raise serializers.ValidationError("Invalid position(s) provided")
        return value


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = [
            "id",
            "name",
            "gym_id",
            "phone_number",
            "birth_date",
        ]
