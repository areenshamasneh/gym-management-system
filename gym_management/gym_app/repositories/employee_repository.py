from sqlalchemy import select, update, delete  # type: ignore
from sqlalchemy.orm import joinedload  # type: ignore

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Employee, Gym


class EmployeeRepository:
    @staticmethod
    def get_gym(gym_id):
        gym = Session.get(Gym, gym_id)
        return gym

    @staticmethod
    def get_all_employees(gym):
        query = select(Employee).filter(Employee.gym_id == gym.id).options(
            joinedload(Employee.gym),
            joinedload(Employee.manager)
        )
        result = Session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_employee_by_id(gym, employee_id):
        query = select(Employee).filter(Employee.id == employee_id, Employee.gym_id == gym.id).options(
            joinedload(Employee.gym), joinedload(Employee.manager))
        result = Session.execute(query)
        employee = result.scalar_one_or_none()
        return employee

    @staticmethod
    def create_employee(gym, data):
        employee = Employee(
            name=data.get("name"),
            gym_id=gym.id,
            manager_id=data.get("manager_id"),
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
            phone_number=data.get("phone_number", ""),
            email=data.get("email"),
            positions=data.get("positions", ""),
        )
        Session.add(employee)
        return employee

    @staticmethod
    def update_employee(gym, employee_id, data):
        update_data = {k: v for k, v in data.items() if k not in ['gym'] and v is not None}

        stmt = (
            update(Employee)
            .where(Employee.id == employee_id, Employee.gym_id == gym.id)
            .values(**update_data)
            .execution_options(synchronize_session="evaluate")
        )
        Session.execute(stmt)
        return Session.execute(
            select(Employee).filter(Employee.id == employee_id, Employee.gym_id == gym.id)
        ).scalar_one_or_none()

    @staticmethod
    def delete_employee(gym, employee_id):
        stmt = (
            delete(Employee)
            .where(Employee.id == employee_id, Employee.gym_id == gym.id)
        )
        Session.execute(stmt)
        return True
