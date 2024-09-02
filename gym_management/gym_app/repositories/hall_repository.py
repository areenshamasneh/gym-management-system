from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import joinedload

from gym_app.models.models_sqlalchemy import Hall, Gym, HallType
from common.database import Session


class HallRepository:
    @staticmethod
    def get_all_halls(gym_id):
        with Session() as session:
            query = (
                select(Hall)
                .filter(Hall.gym_id == gym_id)
                .options(
                    joinedload(Hall.hall_type),
                    joinedload(Hall.gym)
                )
            )
            result = session.execute(query)
            return result.scalars().all()

    @staticmethod
    def get_hall_by_id(gym_id, hall_id):
        with Session() as session:
            query = (
                select(Hall)
                .filter(Hall.id == hall_id, Hall.gym_id == gym_id)
                .options(
                    joinedload(Hall.hall_type),
                    joinedload(Hall.gym)
                )
            )
            try:
                result = session.execute(query)
                return result.scalar_one()
            except NoResultFound:
                return None

    @staticmethod
    def create_hall(gym_id, data):
        with Session() as session:
            try:
                gym_instance = session.get(Gym, gym_id)
                if gym_instance is None:
                    raise ValueError("Gym not found")

                hall_type_id = data.get("hall_type")
                if hall_type_id is None:
                    raise ValueError("HallType ID is required")

                hall_type_instance = session.get(HallType, int(hall_type_id))
                if hall_type_instance is None:
                    raise ValueError("HallType not found")

                hall = Hall(
                    name=data.get("name"),
                    users_capacity=data.get("users_capacity"),
                    hall_type_id=hall_type_instance.id,
                    gym_id=gym_instance.id
                )
                session.add(hall)
                session.commit()
                session.refresh(hall)
                session.refresh(hall, attribute_names=['gym', 'hall_type'])

                return hall

            except ValueError as e:
                session.rollback()
                print(f"Value error: {e}")
                raise ValueError(f"Value error: {e}")
            except SQLAlchemyError as e:
                session.rollback()
                print(f"Database error: {e}")
                raise ValueError(f"Database error: {e}")
            except Exception as e:
                session.rollback()
                print(f"Unexpected error: {e}")
                raise ValueError(f"An unexpected error occurred: {e}")

    @staticmethod
    def update_hall(gym_id, hall_id, data):
        with Session() as session:
            hall = session.execute(
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
                hall_type_instance = session.get(HallType, data['hall_type'])
                if hall_type_instance:
                    hall.hall_type = hall_type_instance

            if 'gym' in data:
                gym_instance = session.get(Gym, data['gym'])
                if gym_instance:
                    hall.gym = gym_instance

            for attr, value in data.items():
                if hasattr(hall, attr) and attr not in ['hall_type', 'gym']:
                    setattr(hall, attr, value)

            session.commit()
            session.refresh(hall)
            session.refresh(hall, attribute_names=['gym', 'hall_type'])

            return hall

    @staticmethod
    def delete_hall(gym_id, hall_id):
        with Session() as session:
            query = delete(Hall).filter(Hall.id == hall_id, Hall.gym_id == gym_id)
            result = session.execute(query)
            session.commit()
            return result.rowcount > 0
