from sqlalchemy import select, func  # type: ignore
from sqlalchemy.orm import joinedload  # type: ignore

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Admin, Gym


class AdminRepository:
    @staticmethod
    def get_gym(gym_id):
        gym = Session.get(Gym, gym_id)
        return gym

    @staticmethod
    def get_all_admins(gym, filter_criteria=None, offset=0, limit=10):
        query = select(Admin).filter(Admin.gym_id == gym.id).options(joinedload(Admin.gym))

        filters = []
        if filter_criteria:
            if filter_criteria.get('name'):
                filters.append(Admin.name.ilike(f"%{filter_criteria['name']}%"))
            if filter_criteria.get('email'):
                filters.append(Admin.email.ilike(f"%{filter_criteria['email']}%"))
            if filter_criteria.get('phone_number'):
                filters.append(Admin.phone_number.ilike(f"%{filter_criteria['phone_number']}%"))
            if filter_criteria.get('address_city'):
                filters.append(Admin.address_city.ilike(f"%{filter_criteria['address_city']}%"))
            if filter_criteria.get('address_street'):
                filters.append(Admin.address_street.ilike(f"%{filter_criteria['address_street']}%"))

        count_query = select(func.count(Admin.id)).filter(Admin.gym_id == gym.id)
        if filters:
            count_query = count_query.filter(*filters)
        total_admins = Session.execute(count_query).scalar()

        if filters:
            query = query.filter(*filters)
        query = query.offset(offset).limit(limit)
        result = Session.execute(query)
        admins = result.scalars().all()

        return admins, total_admins

    @staticmethod
    def get_admin_by_id(gym, admin_id):
        query = select(Admin).filter(Admin.id == admin_id, Admin.gym_id == gym.id).options(
            joinedload(Admin.gym))
        result = Session.execute(query)
        admin = result.scalar_one_or_none()

        return admin

    @staticmethod
    def create_admin(gym, data):
        admin = Admin(
            name=data.get("name"),
            phone_number=data.get("phone_number", ""),
            email=data.get("email"),
            gym_id=gym.id,
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
        )
        Session.add(admin)
        return admin

    @staticmethod
    def update_admin(gym, admin_id, data):
        admin = Session.query(Admin).filter_by(id=admin_id, gym_id=gym.id).first()
        for key, value in data.items():
            setattr(admin, key, value)

        Session.add(admin)
        return admin

    @staticmethod
    def delete_admin(gym, admin_id):
        admin = Session.query(Admin).filter_by(id=admin_id, gym_id=gym.id).first()
        Session.delete(admin)
        return True
