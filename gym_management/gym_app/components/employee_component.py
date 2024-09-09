from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories import EmployeeRepository


class EmployeeComponent:
    def __init__(self, employee_repository=None, logger=None):
        self.employee_repository = employee_repository or EmployeeRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("EmployeeComponent initialized")

    def fetch_all_employees(self, gym_id):
        self.logger.log_info(f"Fetching all employees for gym_id: {gym_id}")
        gym = self.employee_repository.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        employee = self.employee_repository.get_all_employees(gym)
        if not employee:
            raise ResourceNotFoundException("No Employees found for this gym")
        return employee

    def fetch_employee_by_id(self, gym_id, employee_id):
        self.logger.log_info(f"Fetching employee with ID {employee_id} for gym_id: {gym_id}")
        gym = self.employee_repository.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        employee = self.employee_repository.get_employee_by_id(gym, employee_id)
        if not employee:
            raise ResourceNotFoundException("Employee not found")
        return employee

    def add_employee(self, gym_id, data):
        self.logger.log_info("Adding new employee")
        gym = self.employee_repository.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        employee = self.employee_repository.create_employee(gym, data)
        Session.commit()
        return employee

    def modify_employee(self, gym_id, employee_id, data):
        self.logger.log_info(f"Modifying employee ID {employee_id} for gym_id: {gym_id}")
        gym = self.employee_repository.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        employee = self.employee_repository.update_employee(gym, employee_id, data)
        if not employee:
            raise ResourceNotFoundException("Employee not found")
        Session.commit()
        return employee

    def remove_employee(self, gym_id, employee_id):
        self.logger.log_info(f"Removing employee ID {employee_id} for gym_id: {gym_id}")
        gym = self.employee_repository.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        success = self.employee_repository.delete_employee(gym, employee_id)
        if not success:
            raise ResourceNotFoundException("Employee not found")
        Session.commit()
        return success
