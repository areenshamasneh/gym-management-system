from sqlalchemy import func
from gym_app.models.models_sqlalchemy import Gym


class GymRepository:
    @staticmethod
    def get_all_gyms(session, offset=0, limit=10):
        total_gyms = session.query(func.count(Gym.id)).scalar()
        gyms = session.query(Gym).offset(offset).limit(limit).all()
        return gyms, total_gyms

    @staticmethod
    def get_gym_by_id(session, pk):
        return session.query(Gym).get(pk)

    @staticmethod
    def create_gym(session, data):
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
    def update_gym(session, pk, data):
        gym = session.query(Gym).get(pk)
        if gym:
            for key, value in data.items():
                setattr(gym, key, value)
            return gym
        return None

    @staticmethod
    def delete_gym(session, pk):
        gym = session.query(Gym).get(pk)
        if gym:
            session.delete(gym)
            return True
        return False
