from sqlalchemy import func

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Gym


class GymRepository:
    @staticmethod
    def get_all_gyms(offset=0, limit=10):
        total_gyms = Session.query(func.count(Gym.id)).scalar()
        gyms = Session.query(Gym).offset(offset).limit(limit).all()
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
        gym = Session.get(Gym, pk)
        for key, value in data.items():
            setattr(gym, key, value)
        return gym

    @staticmethod
    def delete_gym(pk):
        gym = Session.get(Gym, pk)
        if not gym:
            return False
        Session.delete(gym)
        return True
