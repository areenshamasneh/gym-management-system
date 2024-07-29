from gym_app.repositories.employee_repository import EmployeeRepository
from gym_app.logging import SimpleLogger


class EmployeeComponent:
    def __init__(self, employee_repository=None, logger=None):
        self.employee_repository = employee_repository or EmployeeRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("EmployeeComponent initialized")

    def fetch_all_employees(self, gym_id):
        try:
            self.logger.log_info(f"Fetching all employees for gym_id: {gym_id}")
            employees = self.employee_repository.get_all_employees(gym_id)
            return employees
        except Exception as e:
            self.logger.log_error(
                f"Error fetching all employees for gym_id: {gym_id}: {str(e)}"
            )
            raise

    def fetch_employee_by_id(self, gym_id, employee_id):
        try:
            self.logger.log_info(
                f"Fetching employee by ID {employee_id} for gym_id: {gym_id}"
            )
            employee = self.employee_repository.get_employee_by_id(gym_id, employee_id)
            return employee
        except Exception as e:
            self.logger.log_error(
                f"Unexpected error fetching employee by ID {employee_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise

    def add_employee(self, gym_id, data):
        try:
            self.logger.log_info(f"Adding new employee for gym_id: {gym_id}")
            employee = self.employee_repository.create_employee(gym_id, data)
            return employee
        except Exception as e:
            self.logger.log_error(
                f"Error adding employee for gym_id: {gym_id}: {str(e)}"
            )
            raise

    def modify_employee(self, gym_id, employee_id, data):
        try:
            self.logger.log_info(
                f"Modifying employee ID {employee_id} for gym_id: {gym_id}"
            )
            updated_employee = self.employee_repository.update_employee(
                gym_id, employee_id, data
            )
            return updated_employee
        except Exception as e:
            self.logger.log_error(
                f"Error modifying employee ID {employee_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise

    def remove_employee(self, gym_id, employee_id):
        try:
            self.logger.log_info(
                f"Removing employee ID {employee_id} for gym_id: {gym_id}"
            )
            self.employee_repository.delete_employee(gym_id, employee_id)
        except Exception as e:
            self.logger.log_error(
                f"Error removing employee ID {employee_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise
