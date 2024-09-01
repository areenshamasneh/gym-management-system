from sqlalchemy import func
from common import Session
from gym_app.models.models_sqlalchemy import Gym


class GymRepository:
    @staticmethod
    def get_all_gyms(offset=0, limit=10):
        try:
            total_gyms = Session.query(func.count(Gym.id)).scalar()
            gyms = Session.query(Gym).offset(offset).limit(limit).all()
            return gyms, total_gyms
        finally:
            Session.remove()

    @staticmethod
    def get_gym_by_id(pk):
        try:
            return Session.get(Gym, pk)
        finally:
            Session.remove()

    @staticmethod
    def create_gym(data):
        session = Session()
        gym = Gym(
            name=data.get("name"),
            type=data.get("type"),
            description=data.get("description"),
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
        )
        session.add(gym)
        return gym

    @staticmethod
    def update_gym(pk, data):
        session = Session()
        gym = session.get(Gym, pk)
        if gym:
            for key, value in data.items():
                setattr(gym, key, value)
            return gym
        return None

    @staticmethod
    def delete_gym(pk):
        session = Session()
        gym = session.get(Gym, pk)
        if gym:
            session.delete(gym)
            return True
        return False
