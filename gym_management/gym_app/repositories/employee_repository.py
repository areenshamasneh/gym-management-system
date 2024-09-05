from sqlalchemy import select
from sqlalchemy.orm import joinedload

from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.models.models_sqlalchemy import Employee, Gym


class EmployeeRepository:
    @staticmethod
    def get_all_employees(gym_id):
        try:
            gym = Session.get(Gym, gym_id)
            if not gym:
                raise ResourceNotFoundException("Gym not found")

            query = select(Employee).filter(Employee.gym_id == gym_id).options(
                joinedload(Employee.gym),
                joinedload(Employee.manager)
            )
            result = Session.execute(query)
            return result.scalars().all()
        finally:
            Session.remove()

    @staticmethod
    def get_employee_by_id(gym_id, employee_id):
        try:
            gym = Session.get(Gym, gym_id)
            if not gym:
                raise ResourceNotFoundException("Gym not found")

            query = select(Employee).filter(Employee.id == employee_id, Employee.gym_id == gym_id).options(
                joinedload(Employee.gym), joinedload(Employee.manager))
            result = Session.execute(query)
            employee = result.scalar_one_or_none()

            if not employee:
                raise ResourceNotFoundException("Employee not found")

            return employee
        finally:
            Session.remove()

    @staticmethod
    def create_employee(gym_id, data):
        gym = Session.get(Gym, gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

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
        Session.add(employee)
        return employee

    @staticmethod
    def update_employee(employee_id, data):
        employee = Session.query(Employee).get(employee_id)
        if not employee:
            raise ResourceNotFoundException()

        for key, value in data.items():
            setattr(employee, key, value)
        Session.add(employee)
        return employee

    @staticmethod
    def delete_employee(employee_id):
        employee = Session.query(Employee).get(employee_id)
        if not employee:
            raise ResourceNotFoundException()
        Session.delete(employee)
        return True
