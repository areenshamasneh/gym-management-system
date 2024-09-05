from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Member, Gym
from gym_app.exceptions import ResourceNotFoundException


class MemberRepository:
    @staticmethod
    def get_all_members(gym_id):
        try:
            gym = Session.get(Gym, gym_id)
            if not gym:
                raise ResourceNotFoundException("Gym not found")

            query = select(Member).filter(Member.gym_id == gym_id).options(
                joinedload(Member.gym)
            )
            result = Session.execute(query)
            return result.scalars().all()
        finally:
            Session.remove()

    @staticmethod
    def get_member_by_id(gym_id, member_id):
        try:
            gym = Session.get(Gym, gym_id)
            if not gym:
                raise ResourceNotFoundException("Gym not found")

            query = select(Member).filter(Member.id == member_id, Member.gym_id == gym_id).options(
                joinedload(Member.gym)
            )
            result = Session.execute(query)
            member = result.scalar_one_or_none()

            if not member:
                raise ResourceNotFoundException(f"Member with ID {member_id} not found in gym with ID {gym_id}")

            return member
        finally:
            Session.remove()

    @staticmethod
    def create_member(gym_id, data):
        gym = Session.get(Gym, gym_id)
        if gym is None:
            raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")

        if "gym" in data:
            del data["gym"]

        data["gym_id"] = gym_id

        member = Member(**data)
        Session.add(member)
        return member

    @staticmethod
    def update_member(gym_id, member_id, data):
        query = select(Member).filter(Member.id == member_id, Member.gym_id == gym_id)
        member = Session.execute(query).scalar_one_or_none()

        if member is None:
            raise ResourceNotFoundException(
                f"Member with ID {member_id} not found in gym with ID {gym_id}"
                )

        for key, value in data.items():
            if key != "gym" and hasattr(member, key):
                setattr(member, key, value)

        return member

    @staticmethod
    def delete_member(gym_id, member_id):
        query = delete(Member).filter(Member.id == member_id, Member.gym_id == gym_id)
        result = Session.execute(query)
        if result.rowcount == 0:
            raise ResourceNotFoundException(
                    f"Member with ID {member_id} not found in gym with ID {gym_id}"
            )
        return result.rowcount > 0
