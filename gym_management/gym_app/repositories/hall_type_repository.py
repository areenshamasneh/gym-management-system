from sqlalchemy import select, delete

from common.db.database import Session
from gym_app.models.models_sqlalchemy import HallType, Hall


class HallTypeRepository:

    @staticmethod
    def get_all_hall_types():
        query = select(HallType)
        result = Session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_hall_type_by_id(hall_type_id):
        query = select(HallType).filter(HallType.id == hall_type_id)
        result = Session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    def create_hall_type(data):
        existing_hall_type_query = (
            select(HallType)
            .filter(HallType.code == data['code'])
        )
        existing_hall_type = Session.execute(existing_hall_type_query).scalar_one_or_none()
        if existing_hall_type:
            return None
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
                    return None
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
            return None

        query = delete(HallType).filter(HallType.id == hall_type_id)
        result = Session.execute(query)
        return result.rowcount > 0
