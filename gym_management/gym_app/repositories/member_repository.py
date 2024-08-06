from django.db import IntegrityError

from gym_app.exceptions import ResourceNotFoundException, DatabaseException
from gym_app.models import Member, Gym


class MemberRepository:

    @staticmethod
    def get_all_members(gym_id):
        try:
            return Member.objects.filter(gym_id=gym_id)
        except Exception as e:
            raise DatabaseException(f"Error fetching members: {e}")

    @staticmethod
    def get_member_by_id(gym_id, member_id):
        try:
            return Member.objects.get(pk=member_id, gym_id=gym_id)
        except Member.DoesNotExist:
            raise ResourceNotFoundException(f"Member with ID {member_id} not found in gym with ID {gym_id}")

    @staticmethod
    def create_member(gym_id, data):
        try:
            gym_instance = Gym.objects.get(pk=gym_id)
            data["gym_id"] = gym_instance
            return Member.objects.create(**data)
        except Gym.DoesNotExist:
            raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")
        except IntegrityError as e:
            raise DatabaseException(f"Error creating Member: {e}")

    @staticmethod
    def update_member(gym_id, member_id, data):
        try:
            member = Member.objects.get(pk=member_id, gym_id=gym_id)
            for attr, value in data.items():
                if hasattr(member, attr):
                    setattr(member, attr, value)
            member.save()
            return member
        except Member.DoesNotExist:
            raise ResourceNotFoundException(f"Member with ID {member_id} not found in gym with ID {gym_id}")
        except IntegrityError as e:
            raise DatabaseException(f"Error updating Member: {e}")

    @staticmethod
    def delete_member(gym_id, member_id):
        try:
            member = Member.objects.get(pk=member_id, gym_id=gym_id)
            member.delete()
        except Member.DoesNotExist:
            raise ResourceNotFoundException(f"Member with ID {member_id} not found in gym with ID {gym_id}")
        except IntegrityError as e:
            raise DatabaseException(f"Error deleting Member: {e}")
