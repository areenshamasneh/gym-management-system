from sqlalchemy import select
from sqlalchemy.orm import joinedload

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Hall, Gym, HallType


class HallRepository:
    @staticmethod
    def get_gym(gym_id):
        return Session.get(Gym, gym_id)

    @staticmethod
    def get_all_halls(gym):
        query = select(Hall).where(Hall.gym_id == gym.id).options(joinedload(Hall.gym))
        result = Session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_hall_by_id(gym, hall_id):
        query = select(Hall).where(Hall.id == hall_id, Hall.gym_id == gym.id).options(joinedload(Hall.gym))
        result = Session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    def create_hall(gym, data):
        hall_type_id = data.get("hall_type")

        hall_type_instance = Session.get(HallType, int(hall_type_id))
        if hall_type_instance is None:
            return None

        hall = Hall(
            name=data.get("name"),
            users_capacity=data.get("users_capacity"),
            hall_type_id=hall_type_instance.id,
            gym_id=gym.id
        )
        Session.add(hall)
        return hall

    @staticmethod
    def update_hall(gym, hall_id, data):
        query = (
            select(Hall)
            .where(Hall.id == hall_id, Hall.gym_id == gym.id)
            .options(
                joinedload(Hall.hall_type),
                joinedload(Hall.gym)
            )
        )
        hall = Session.execute(query).scalar_one_or_none()

        if hall is None:
            return None

        if 'hall_type' in data:
            hall_type_instance = Session.get(HallType, data['hall_type'])
            if hall_type_instance:
                hall.hall_type = hall_type_instance

        if 'gym' in data:
            gym_instance = Session.get(Gym, data['gym'])
            if gym_instance:
                hall.gym = gym_instance

        for attr, value in data.items():
            if hasattr(hall, attr) and attr not in ['hall_type', 'gym']:
                setattr(hall, attr, value)
        Session.add(hall)
        return hall

    @staticmethod
    def delete_hall(gym, hall_id):
        query = select(Hall).where(Hall.id == hall_id, Hall.gym_id == gym.id)
        hall = Session.execute(query).scalar_one_or_none()
        if not hall:
            return False
        Session.delete(hall)
        return True
