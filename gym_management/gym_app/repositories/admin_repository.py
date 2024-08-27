from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload

from gym_app.models.models_sqlalchemy import Admin, Gym
from gym_management.db_session import SessionLocal


class AdminRepository:
    @staticmethod
    def get_all_admins(gym_id, filter_criteria=None):
        with SessionLocal() as session:
            query = select(Admin).filter(Admin.gym_id == gym_id).options(joinedload(Admin.gym))

            if filter_criteria:
                if filter_criteria.get('name'):
                    query = query.filter(Admin.name.ilike(f"%{filter_criteria['name']}%"))
                if filter_criteria.get('email'):
                    query = query.filter(Admin.email.ilike(f"%{filter_criteria['email']}%"))
                if filter_criteria.get('phone_number'):
                    query = query.filter(Admin.phone_number.ilike(f"%{filter_criteria['phone_number']}%"))
                if filter_criteria.get('address_city'):
                    query = query.filter(Admin.address_city.ilike(f"%{filter_criteria['address_city']}%"))
                if filter_criteria.get('address_street'):
                    query = query.filter(Admin.address_street.ilike(f"%{filter_criteria['address_street']}%"))

            result = session.execute(query)
            return result.scalars().all()

    @staticmethod
    def get_admin_by_id(gym_id, admin_id):
        with SessionLocal() as session:
            try:
                query = select(Admin).filter(Admin.id == admin_id, Admin.gym_id == gym_id).options(
                    joinedload(Admin.gym))
                result = session.execute(query)
                return result.scalar_one()
            except NoResultFound:
                return None

    @staticmethod
    def create_admin(gym_id, data):
        with SessionLocal() as session:
            gym = session.get(Gym, gym_id)
            if gym is None:
                raise ValueError("Gym not found")
            admin = Admin(
                name=data.get("name"),
                phone_number=data.get("phone_number", ""),
                email=data.get("email"),
                gym_id=gym_id,
                address_city=data.get("address_city"),
                address_street=data.get("address_street"),
            )
            session.add(admin)
            session.commit()
            session.refresh(admin)
            session.refresh(admin, attribute_names=['gym'])

            return admin

    @staticmethod
    def update_admin(gym_id, admin_id, data):
        with SessionLocal() as session:
            query = select(Admin).filter(Admin.id == admin_id, Admin.gym_id == gym_id)
            admin = session.execute(query).scalar_one_or_none()

            if admin is None:
                return None

            if 'name' in data:
                admin.name = data['name']
            if 'phone_number' in data:
                admin.phone_number = data['phone_number']
            if 'email' in data:
                admin.email = data['email']
            if 'address_city' in data:
                admin.address_city = data['address_city']
            if 'address_street' in data:
                admin.address_street = data['address_street']

            session.commit()
            session.refresh(admin)
            session.refresh(admin, attribute_names=['gym'])

            return admin

    @staticmethod
    def delete_admin(gym_id, admin_id):
        with SessionLocal() as session:
            query = delete(Admin).filter(Admin.id == admin_id, Admin.gym_id == gym_id)
            result = session.execute(query)
            session.commit()
            return result.rowcount > 0
