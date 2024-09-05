from sqlalchemy import select
from sqlalchemy.orm import joinedload

from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.models.models_sqlalchemy import Hall, Gym, HallType


class HallRepository:
    @staticmethod
    def get_all_halls(gym_id):
        gym = Session.get(Gym, gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        query = select(Hall).filter(Hall.gym_id == gym_id).options(joinedload(Hall.gym))
        result = Session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_hall_by_id(gym_id, hall_id):
        gym = Session.get(Gym, gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        query = select(Hall).filter(Hall.id == hall_id, Hall.gym_id == gym_id).options(joinedload(Hall.gym))
        result = Session.execute(query)
        hall = result.scalar_one_or_none()
        if not hall:
            raise ResourceNotFoundException("Hall not found")
        return hall

    @staticmethod
    def create_hall(gym_id, data):
        gym_instance = Session.get(Gym, gym_id)
        if gym_instance is None:
            raise ValueError("Gym not found")

        hall_type_id = data.get("hall_type")
        if hall_type_id is None:
            raise ValueError("HallType ID is required")

        hall_type_instance = Session.get(HallType, int(hall_type_id))
        if hall_type_instance is None:
            raise ValueError("HallType not found")

        hall = Hall(
            name=data.get("name"),
            users_capacity=data.get("users_capacity"),
            hall_type_id=hall_type_instance.id,
            gym_id=gym_instance.id
        )
        Session.add(hall)
        return hall

    @staticmethod
    def update_hall(gym_id, hall_id, data):
        hall = Session.execute(
            select(Hall)
            .filter(Hall.id == hall_id, Hall.gym_id == gym_id)
            .options(
                joinedload(Hall.hall_type),
                joinedload(Hall.gym)
            )
        ).scalar_one_or_none()

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
    def delete_hall(gym_id, hall_id):
        hall = Session.query(Hall).filter_by(id=hall_id, gym_id=gym_id).one_or_none()
        if not hall:
            raise ResourceNotFoundException("Hall not found")
        Session.delete(hall)
        return True
