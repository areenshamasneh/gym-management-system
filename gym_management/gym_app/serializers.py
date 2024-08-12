from pydantic import ValidationError
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
from gym_app.models.hall_type_model import HallTypeModel


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ["id", "name", "type", "description", "address_city", "address_street"]


class HallTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HallType
        fields = "__all__"

    def validate(self, data):
        try:
            HallTypeModel(**data)
        except ValidationError as e:
            raise serializers.ValidationError(e.errors())
        return data


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
    gym = GymSerializer(read_only=True)
    hall_type = serializers.PrimaryKeyRelatedField(queryset=HallType.objects.all(), write_only=True)
    hall__type = HallTypeSerializer(source='hall_type', read_only=True)

    class Meta:
        model = Hall
        fields = ["id", "name", "users_capacity", "hall_type", "hall__type", "gym"]


class HallMachineSerializer(serializers.ModelSerializer):
    hall = HallSerializer(read_only=True)
    machine = MachineSerializer(read_only=True)

    class Meta:
        model = HallMachine
        fields = ["id", "hall", "machine", "name", "uid"]


class AdminSerializer(serializers.ModelSerializer):
    gym = GymSerializer(read_only=True)

    class Meta:
        model = Admin
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "gym",
            "address_city",
            "address_street",
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    gym = GymSerializer()
    manager = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "gym",
            "manager",
            "address_city",
            "address_street",
            "phone_number",
            "email",
            "positions",
        ]

    @staticmethod
    def get_manager(obj):
        if obj.manager:
            return EmployeeSerializer(obj.manager).data
        return None

    @staticmethod
    def validate_email(value):
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    @staticmethod
    def validate_positions(value):
        positions_list = [pos.strip() for pos in value.split(",") if pos.strip()]
        valid_positions = {"cleaner", "trainer", "system_worker"}
        if not set(positions_list).issubset(valid_positions):
            raise serializers.ValidationError("Invalid position(s) provided")
        return value


class MemberSerializer(serializers.ModelSerializer):
    gym = GymSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'name', 'gym', 'phone_number', 'birth_date']

    def create(self, validated_data):
        gym_id = self.context['gym_id']
        gym = Gym.objects.get(id=gym_id)

        member = Member.objects.create(gym=gym, **validated_data)
        return member
