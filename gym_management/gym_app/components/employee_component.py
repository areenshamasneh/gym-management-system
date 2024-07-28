from gym_app.repositories.employee_repository import EmployeeRepository


class EmployeeComponent:

    def fetch_all_employees(gym_id):
        return EmployeeRepository.get_all_employees(gym_id)

    def fetch_employee_by_id(gym_id, employee_id):
        return EmployeeRepository.get_employee_by_id(gym_id, employee_id)

    def add_employee(gym_id, data):
        return EmployeeRepository.create_employee(gym_id, data)

    def modify_employee(gym_id, employee_id, data):
        try:
            return EmployeeRepository.update_employee(gym_id, employee_id, data)
        except ValueError as e:
            # Re-raise the exception for clarity in debugging
            raise ValueError(str(e))

    def remove_employee(gym_id, employee_id):
        return EmployeeRepository.delete_employee(gym_id, employee_id)
