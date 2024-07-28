from gym_app.repositories.employee_repository import EmployeeRepository


class EmployeeComponent:

    def fetch_all_employees():
        return EmployeeRepository.get_all_employees()

    def fetch_employee_by_id(employee_id):
        return EmployeeRepository.get_employee_by_id(employee_id)

    def add_employee(data):
        return EmployeeRepository.create_employee(data)

    def modify_employee(employee_id, data):
        return EmployeeRepository.update_employee(employee_id, data)

    def remove_employee(employee_id):
        return EmployeeRepository.delete_employee(employee_id)
