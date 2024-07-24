from gym_app.models import Member, Gym
from django.shortcuts import get_object_or_404


class MemberRepository:
    @staticmethod
    def get_all_members():
        return Member.objects.all()

    @staticmethod
    def get_member_by_id(member_id):
        return get_object_or_404(Member, pk=member_id)

    @staticmethod
    def create_member(data):
        gym_id = data.pop("gym", None)
        if gym_id:
            gym_instance = get_object_or_404(Gym, pk=gym_id)
            data["gym"] = gym_instance
        else:
            raise ValueError("Gym field is required")

        return Member.objects.create(**data)

    @staticmethod
    def update_member(member_id, data):
        member = get_object_or_404(Member, pk=member_id)
        gym_id = data.pop("gym", None)

        if gym_id:
            gym_instance = get_object_or_404(Gym, pk=gym_id)
            data["gym"] = gym_instance

        for attr, value in data.items():
            if hasattr(member, attr):
                setattr(member, attr, value)

        member.save()
        return member

    @staticmethod
    def delete_member(member_id):
        member = get_object_or_404(Member, pk=member_id)
        member.delete()
