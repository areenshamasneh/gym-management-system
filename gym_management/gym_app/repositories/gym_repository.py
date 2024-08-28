from sqlalchemy import func

from common import SessionLocal
from gym_app.models.models_sqlalchemy import Gym


class GymRepository:
    @staticmethod
    def get_all_gyms(offset=0, limit=10):
        with SessionLocal() as session:
            total_gyms = session.query(func.count(Gym.id)).scalar()
            gyms = session.query(Gym).offset(offset).limit(limit).all()
            return gyms, total_gyms

    @staticmethod
    def get_gym_by_id(pk):
        with SessionLocal() as session:
            return session.get(Gym, pk)

    @staticmethod
    def create_gym(data):
        print(f"Request data: {data}")  #
        with SessionLocal() as session:
            gym = Gym(
                name=data.get("name"),
                type=data.get("type"),
                description=data.get("description"),
                address_city=data.get("address_city"),
                address_street=data.get("address_street"),
            )
            session.add(gym)
            session.commit()
            session.refresh(gym)
            return gym

    @staticmethod
    def update_gym(pk, data):
        with SessionLocal() as session:
            gym = session.get(Gym, pk)
            if gym:
                for key, value in data.items():
                    setattr(gym, key, value)
                session.commit()
                session.refresh(gym)
                return gym
            return None

    @staticmethod
    def delete_gym(pk):
        with SessionLocal() as session:
            gym = session.get(Gym, pk)
            if gym:
                session.delete(gym)
                session.commit()
                return True
            return False
