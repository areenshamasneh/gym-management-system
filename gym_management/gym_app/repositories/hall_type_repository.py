from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.orm import joinedload

from common.db.database import Session
from gym_app.exceptions import DatabaseException
from gym_app.models.models_sqlalchemy import HallType, Hall


class HallTypeRepository:

    @staticmethod
    def get_all_hall_types():
        try:
            query = select(HallType)
            result = Session.execute(query)
            return result.scalars().all()
        finally:
            Session.remove()

    @staticmethod
    def get_hall_type_by_id(hall_type_id):
        try:
            query = select(HallType).filter(HallType.id == hall_type_id)
            result = Session.execute(query)
            return result.scalar_one_or_none()
        finally:
            Session.remove()

    @staticmethod
    def create_hall_type(data):
        hall_type = HallType(**data)
        Session.add(hall_type)
        return hall_type

    @staticmethod
    def update_hall_type(hall_type_id, data):
        query = select(HallType).filter(HallType.id == hall_type_id)
        hall_type = Session.execute(query).scalar_one_or_none()

        if hall_type is None:
            return None

        if 'code' in data:
            if data['code'] != hall_type.code:
                existing_hall_type_query = (
                    select(HallType)
                    .filter(HallType.code == data['code'])
                    .filter(HallType.id != hall_type_id)
                )
                existing_hall_type = Session.execute(existing_hall_type_query).scalar_one_or_none()
                if existing_hall_type:
                    raise DatabaseException("Code already exists for another hall type.")
                hall_type.code = data['code']

        if 'name' in data:
            hall_type.name = data['name']

        if 'type_description' in data:
            hall_type.type_description = data['type_description']

        Session.add(hall_type)
        return hall_type

    @staticmethod
    def delete_hall_type(hall_type_id):
        halls_query = select(Hall).filter(Hall.hall_type_id == hall_type_id)
        associated_halls = Session.execute(halls_query).scalars().all()

        if associated_halls:
            raise DatabaseException("Cannot delete HallType because it is still in use by Halls.")

        query = delete(HallType).filter(HallType.id == hall_type_id)
        result = Session.execute(query)
        return result.rowcount > 0
