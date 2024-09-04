from sqlalchemy.exc import NoResultFound

from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories import EmployeeRepository


class EmployeeComponent:
    def __init__(self, employee_repository=None, logger=None):
        self.employee_repository = employee_repository or EmployeeRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("EmployeeComponent initialized")

    def fetch_all_employees(self, gym_id):
        try:
            self.logger.log_info(f"Fetching all employees for gym_id: {gym_id}")
            employees = self.employee_repository.get_all_employees(gym_id)
            if len(employees) == 0:
                raise ResourceNotFoundException(f"There are no employees for gym_id: {gym_id}")
            return employees
        except ResourceNotFoundException as e:
            self.logger.log_error(
                f"Resource not found for gym_id: {gym_id}: {str(e)}"
            )
            raise ResourceNotFoundException(f"Resource not found for gym_id: {gym_id}")
        except Exception as e:
            self.logger.log_error(
                f"Error fetching all employees for gym_id: {gym_id}: {str(e)}"
            )
            raise Exception("An error occurred while fetching all employees.")

    def fetch_employee_by_id(self, gym_id, employee_id):
        try:
            self.logger.log_info(f"Fetching employee with ID {employee_id}")
            employee = self.employee_repository.get_employee_by_id(gym_id, employee_id)
            if employee is None:
                raise ResourceNotFoundException(
                    f"Employee with ID {employee_id} does not exist for gym_id: {gym_id}"
                )
            return employee
        except ResourceNotFoundException as e:
            self.logger.log_error(f"Resource not found: {str(e)}")
            raise ResourceNotFoundException(f"Employee with ID {employee_id} does not exist for gym_id: {gym_id}")
        except Exception as e:
            self.logger.log_error(f"Error fetching employee: {str(e)}")
            raise Exception("Error fetching employee")

    def add_employee(self, gym_id, data):
        try:
            self.logger.log_info(f"Adding new employee for gym_id: {gym_id}")
            return self.employee_repository.create_employee(gym_id, data)
        except Exception as e:
            self.logger.log_error(
                f"Error adding employee for gym_id: {gym_id}: {str(e)}"
            )
            raise Exception("Error adding employee")

    def modify_employee(self, gym_id, employee_id, data):
        try:
            self.logger.log_info(
                f"Modifying employee ID {employee_id} for gym_id: {gym_id}"
            )
            return self.employee_repository.update_employee(gym_id, employee_id, data)
        except NoResultFound:
            self.logger.log_error(
                f"Employee with ID {employee_id} does not exist for gym_id: {gym_id}"
            )
            raise ResourceNotFoundException(
                f"Employee with ID {employee_id} does not exist"
            )
        except Exception as e:
            self.logger.log_error(
                f"Error modifying employee ID {employee_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise Exception("Error modifying employee")

    def remove_employee(self, gym_id, employee_id):
        try:
            self.logger.log_info(
                f"Removing employee ID {employee_id} for gym_id: {gym_id}"
            )
            self.employee_repository.delete_employee(gym_id, employee_id)
        except NoResultFound:
            self.logger.log_error(
                f"Employee with ID {employee_id} does not exist for gym_id: {gym_id}"
            )
            raise ResourceNotFoundException(
                f"Employee with ID {employee_id} does not exist"
            )
        except Exception as e:
            self.logger.log_error(
                f"Error removing employee ID {employee_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise Exception("Error removing employee")
