from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import joinedload

from gym_app.exceptions import ResourceNotFoundException, DatabaseException
from gym_app.models.models_sqlalchemy import Member, Gym
from common.database import Session


class MemberRepository:

    @staticmethod
    def get_all_members(gym_id):
        with Session() as session:
            query = select(Member).filter(Member.gym_id == gym_id).options(
                joinedload(Member.gym)
            )
            result = session.execute(query)
            return result.scalars().all()

    @staticmethod
    def get_member_by_id(gym_id, member_id):
        with Session() as session:
            query = select(Member).filter(Member.id == member_id, Member.gym_id == gym_id).options(
                joinedload(Member.gym)
            )
            try:
                result = session.execute(query)
                return result.scalar_one()
            except NoResultFound:
                raise ResourceNotFoundException(
                    f"Member with ID {member_id} not found in gym with ID {gym_id}"
                )

    @staticmethod
    def create_member(gym_id, data):
        with Session() as session:
            gym = session.get(Gym, gym_id)
            if gym is None:
                raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")

            if "gym" in data:
                del data["gym"]

            data["gym_id"] = gym_id

            member = Member(**data)
            try:
                session.add(member)
                session.commit()
                session.refresh(member)
                session.refresh(member, attribute_names=['gym'])
                return member
            except IntegrityError as e:
                session.rollback()
                raise DatabaseException(f"Error creating Member: {e.orig}")

    @staticmethod
    def update_member(gym_id, member_id, data):
        with Session() as session:
            query = select(Member).filter(Member.id == member_id, Member.gym_id == gym_id)
            member = session.execute(query).scalar_one_or_none()

            if member is None:
                raise ResourceNotFoundException(
                    f"Member with ID {member_id} not found in gym with ID {gym_id}"
                )

            for key, value in data.items():
                if key != "gym" and hasattr(member, key):
                    setattr(member, key, value)

            try:
                session.commit()
                session.refresh(member)
                session.refresh(member, attribute_names=['gym'])
                return member
            except IntegrityError as e:
                session.rollback()
                raise DatabaseException(f"Error updating Member: {e.orig}")

    @staticmethod
    def delete_member(gym_id, member_id):
        with Session() as session:
            query = delete(Member).filter(Member.id == member_id, Member.gym_id == gym_id)
            result = session.execute(query)
            session.commit()
            if result.rowcount == 0:
                raise ResourceNotFoundException(
                    f"Member with ID {member_id} not found in gym with ID {gym_id}"
                )
            return result.rowcount > 0
