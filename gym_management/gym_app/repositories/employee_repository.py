from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload

from gym_app.models.models_sqlalchemy import Employee, Gym
from gym_management.settings import SessionLocal


class EmployeeRepository:
    @staticmethod
    def get_all_employees(gym_id):
        with SessionLocal() as session:
            query = select(Employee).filter(Employee.gym_id == gym_id).options(
                joinedload(Employee.gym),
                joinedload(Employee.manager)
            )

            result = session.execute(query)
            return result.scalars().all()

    @staticmethod
    def get_employee_by_id(gym_id, employee_id):
        with SessionLocal() as session:
            query = select(Employee).filter(Employee.id == employee_id, Employee.gym_id == gym_id).options(
                joinedload(Employee.gym), joinedload(Employee.manager))
            result = session.execute(query)
            employee = result.scalar_one_or_none()
            return employee

    @staticmethod
    def create_employee(gym_id, data):
        with SessionLocal() as session:
            gym = session.get(Gym, gym_id)
            if gym is None:
                raise ValueError("Gym not found")

            employee = Employee(
                name=data.get("name"),
                gym_id=gym_id,
                manager_id=data.get("manager_id"),
                address_city=data.get("address_city"),
                address_street=data.get("address_street"),
                phone_number=data.get("phone_number", ""),
                email=data.get("email"),
                positions=data.get("positions", ""),
            )
            session.add(employee)
            session.commit()
            session.refresh(employee)
            session.refresh(employee, attribute_names=['gym', 'manager'])

            return employee

    @staticmethod
    def update_employee(gym_id, employee_id, data):
        with SessionLocal() as session:
            query = select(Employee).filter(Employee.id == employee_id, Employee.gym_id == gym_id).options(
                joinedload(Employee.manager))
            employee = session.execute(query).scalar_one_or_none()

            if employee is None:
                return None

            if 'name' in data:
                employee.name = data['name']
            if 'manager_id' in data:
                employee.manager_id = data.get('manager_id')
            if 'address_city' in data:
                employee.address_city = data['address_city']
            if 'address_street' in data:
                employee.address_street = data['address_street']
            if 'phone_number' in data:
                employee.phone_number = data.get('phone_number', "")
            if 'email' in data:
                employee.email = data['email']
            if 'positions' in data:
                employee.positions = data.get('positions', "")

            session.commit()
            session.refresh(employee)
            session.refresh(employee, attribute_names=['gym'])

            return employee

    @staticmethod
    def delete_employee(gym_id, employee_id):
        with SessionLocal() as session:
            query = delete(Employee).filter(Employee.id == employee_id, Employee.gym_id == gym_id)
            result = session.execute(query)
            session.commit()
            return result.rowcount > 0
