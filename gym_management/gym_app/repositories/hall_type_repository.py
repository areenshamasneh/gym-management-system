from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from gym_app.exceptions import DatabaseException
from gym_app.models.models_sqlalchemy import HallType, Hall
from gym_management.db_session import SessionLocal


class HallTypeRepository:

    @staticmethod
    def get_all_hall_types():
        with SessionLocal() as session:
            query = select(HallType)
            result = session.execute(query)
            return result.scalars().all()

    @staticmethod
    def get_hall_type_by_id(hall_type_id):
        with SessionLocal() as session:
            query = select(HallType).filter(HallType.id == hall_type_id)
            try:
                result = session.execute(query)
                return result.scalar_one()
            except NoResultFound:
                return None

    @staticmethod
    def create_hall_type(data):
        with SessionLocal() as session:
            hall_type = HallType(**data)
            try:
                session.add(hall_type)
                session.commit()
                session.refresh(hall_type)
                return hall_type
            except IntegrityError as e:
                session.rollback()
                raise DatabaseException(f"Integrity error: {e.orig}")

    @staticmethod
    def update_hall_type(hall_type_id, data):
        with SessionLocal() as session:
            query = select(HallType).filter(HallType.id == hall_type_id)
            hall_type = session.execute(query).scalar_one_or_none()

            if hall_type is None:
                return None

            if 'code' in data:
                if data['code'] != hall_type.code:
                    existing_hall_type_query = (
                        select(HallType)
                        .filter(HallType.code == data['code'])
                        .filter(HallType.id != hall_type_id)
                    )
                    existing_hall_type = session.execute(existing_hall_type_query).scalar_one_or_none()
                    if existing_hall_type:
                        raise DatabaseException("Code already exists for another hall type.")
                    hall_type.code = data['code']

            if 'name' in data:
                hall_type.name = data['name']

            if 'type_description' in data:
                hall_type.type_description = data['type_description']

            try:
                session.commit()
                session.refresh(hall_type)
                return hall_type
            except IntegrityError as e:
                session.rollback()
                raise DatabaseException(f"Integrity error: {e.orig}")

    @staticmethod
    def delete_hall_type(hall_type_id):
        with SessionLocal() as session:
            halls_query = select(Hall).filter(Hall.hall_type_id == hall_type_id)
            associated_halls = session.execute(halls_query).scalars().all()

            if associated_halls:
                raise DatabaseException("Cannot delete HallType because it is still in use by Halls.")

            query = delete(HallType).filter(HallType.id == hall_type_id)
            result = session.execute(query)
            session.commit()
            return result.rowcount > 0
