from sqlalchemy import select, func, update, delete  # type: ignore
from sqlalchemy.orm import joinedload  # type: ignore

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Gym


class GymRepository:
    @staticmethod
    def get_all_gyms(offset=0, limit=10):
        count_query = select(func.count(Gym.id))
        total_gyms = Session.execute(count_query).scalar()

        gyms_query = (
            select(Gym)
            .offset(offset)
            .limit(limit)
        )
        gyms_result = Session.execute(gyms_query)
        gyms = gyms_result.scalars().all()

        return gyms, total_gyms

    @staticmethod
    def get_gym_by_id(pk):
        gym = Session.get(Gym, pk)
        return gym

    @staticmethod
    def create_gym(data):
        gym = Gym(
            name=data.get("name"),
            type=data.get("type"),
            description=data.get("description"),
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
        )
        Session.add(gym)
        return gym

    @staticmethod
    def update_gym(pk, data):
        stmt = (
            update(Gym)
            .where(Gym.id == pk)
            .values(**data)
            .execution_options(synchronize_session="evaluate")
        )
        Session.execute(stmt)

        return Session.execute(
            select(Gym).filter(Gym.id == pk)
        ).scalar_one_or_none()

    @staticmethod
    def delete_gym(pk):
        stmt = (
            delete(Gym)
            .where(Gym.id == pk)
        )
        Session.execute(stmt)
        return True
