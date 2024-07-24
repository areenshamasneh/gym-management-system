from gym_app.repositories.employee_repository import EmployeeRepository


class EmployeeComponent:
    @staticmethod
    def fetch_all_employees():
        return EmployeeRepository.get_all_employees()

    @staticmethod
    def fetch_employee_by_id(employee_id):
        return EmployeeRepository.get_employee_by_id(employee_id)

    @staticmethod
    def add_employee(data):
        return EmployeeRepository.create_employee(data)

    @staticmethod
    def modify_employee(employee_id, data):
        return EmployeeRepository.update_employee(employee_id, data)

    @staticmethod
    def remove_employee(employee_id):
        return EmployeeRepository.delete_employee(employee_id)
