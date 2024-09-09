from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Member, Gym


class MemberRepository:
    @staticmethod
    def get_gym(gym_id):
        return Session.get(Gym, gym_id)

    @staticmethod
    def get_all_members(gym):
        query = (
            select(Member)
            .where(Member.gym_id == gym.id)
            .options(joinedload(Member.gym))
        )
        result = Session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_member_by_id(gym, member_id):
        query = (
            select(Member)
            .where(Member.id == member_id, Member.gym_id == gym.id)
            .options(joinedload(Member.gym))
        )
        result = Session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    def create_member(gym, data):
        if "gym" in data:
            del data["gym"]

        data["gym_id"] = gym.id
        member = Member(**data)
        Session.add(member)
        return member

    @staticmethod
    def update_member(gym, member_id, data):
        query = (
            select(Member)
            .where(Member.id == member_id, Member.gym_id == gym.id)
        )
        member = Session.execute(query).scalar_one_or_none()

        if member:
            for key, value in data.items():
                if key != "gym" and hasattr(member, key):
                    setattr(member, key, value)
            return member

    @staticmethod
    def delete_member(gym, member_id):
        query = (
            delete(Member)
            .where(Member.id == member_id, Member.gym_id == gym.id)
        )
        result = Session.execute(query)
        return result.rowcount > 0
