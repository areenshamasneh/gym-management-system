from common.db.database import Session
from gym_app.logging import SimpleLogger
from gym_app.repositories import EmployeeRepository


class EmployeeComponent:
    def __init__(self, employee_repository=None, logger=None):
        self.employee_repository = employee_repository or EmployeeRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("EmployeeComponent initialized")

    def fetch_all_employees(self, gym_id):
        self.logger.log_info(f"Fetching all employees for gym_id: {gym_id}")
        return self.employee_repository.get_all_employees(gym_id)

    def fetch_employee_by_id(self, gym_id, employee_id):
        self.logger.log_info(f"Fetching employee with ID {employee_id} for gym_id: {gym_id}")
        return self.employee_repository.get_employee_by_id(gym_id, employee_id)

    def add_employee(self, gym_id, data):
        session = Session()
        self.logger.log_info("Adding new employee")
        employee = self.employee_repository.create_employee(gym_id, data)
        session.commit()
        return employee

    def modify_employee(self, gym_id, employee_id, data):
        session = Session()
        self.logger.log_info(f"Modifying employee ID {employee_id} for gym_id: {gym_id}")
        employee = self.employee_repository.update_employee(employee_id, data)
        if employee:
            session.commit()
            return employee
        return None

    def remove_employee(self, gym_id, employee_id):
        session = Session()
        self.logger.log_info(f"Removing employee ID {employee_id} for gym_id: {gym_id}")
        success = self.employee_repository.delete_employee(employee_id)
        if success:
            session.commit()
            return success
        return False
