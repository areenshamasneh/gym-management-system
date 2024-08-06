
from gym_app.exceptions import ResourceNotFoundException
from gym_app.models import Employee, Gym


class EmployeeRepository:

    @staticmethod
    def get_all_employees(gym_id):
        return Employee.objects.filter(gym_id=gym_id)

    @staticmethod
    def get_employee_by_id(gym_id, employee_id):
        employee = Employee.objects.filter(pk=employee_id, gym_id=gym_id).first()
        if employee is None:
            raise ResourceNotFoundException(f"Employee with ID {employee_id} not found for gym_id {gym_id}")
        return employee

    @staticmethod
    def create_employee(gym_id, data):
        gym = Gym.objects.get(pk=gym_id)
        if not Gym.objects.filter(pk=gym_id).exists():
            raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")
        return Employee.objects.create(
            name=data["name"],
            gym_id=gym,
            manager_id=data.get("manager_id"),
            address_city=data["address_city"],
            address_street=data["address_street"],
            phone_number=data.get("phone_number", ""),
            email=data["email"],
            positions=data.get("positions", ""),
        )

    @staticmethod
    def update_employee(gym_id, employee_id, data):
        Employee.objects.filter(pk=employee_id, gym_id=gym_id).update(
            name=data.get("name"),
            manager_id=data.get("manager_id"),
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
            phone_number=data.get("phone_number", ""),
            email=data.get("email"),
            positions=data.get("positions", ""),
        )
        return EmployeeRepository.get_employee_by_id(gym_id, employee_id)

    @staticmethod
    def delete_employee(gym_id, employee_id):
        if not Employee.objects.filter(pk=employee_id, gym_id=gym_id).exists():
            raise ResourceNotFoundException(f"Employee with ID {employee_id} not found for gym_id {gym_id}")
        Employee.objects.filter(pk=employee_id, gym_id=gym_id).delete()
