from django.shortcuts import get_object_or_404

from gym_app.models import Member, Gym


class MemberRepository:

    def get_all_members(self, gym_id):
        return Member.objects.filter(gym_id=gym_id)

    def get_member_by_id(self, gym_id, member_id):
        return get_object_or_404(Member, pk=member_id, gym_id=gym_id)

    def create_member(self, gym_id, data):
        gym_instance = get_object_or_404(Gym, pk=gym_id)
        data["gym_id"] = gym_instance
        return Member.objects.create(**data)

    def update_member(self, gym_id, member_id, data):
        member = get_object_or_404(Member, pk=member_id, gym_id=gym_id)
        for attr, value in data.items():
            if hasattr(member, attr):
                setattr(member, attr, value)
        member.save()
        return member

    def delete_member(self, gym_id, member_id):
        member = get_object_or_404(Member, pk=member_id, gym_id=gym_id)
        member.delete()
