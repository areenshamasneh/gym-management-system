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
        manager = None
        if 'manager' in data:
            try:
                manager = Employee.objects.get(pk=data['manager'])
            except Employee.DoesNotExist:
                raise ResourceNotFoundException(f"Manager with ID {data['manager_id']} not found")
        return Employee.objects.create(
            name=data["name"],
            gym=gym,
            manager=manager,
            address_city=data["address_city"],
            address_street=data["address_street"],
            phone_number=data.get("phone_number", ""),
            email=data["email"],
            positions=data.get("positions", ""),
        )

    @staticmethod
    def update_employee(gym_id, employee_id, data):
        employee = Employee.objects.filter(pk=employee_id, gym_id=gym_id).first()
        if employee is None:
            raise ResourceNotFoundException(f"Employee with ID {employee_id} not found for gym_id {gym_id}")

        if 'name' in data:
            employee.name = data['name']
        if 'manager' in data:
            manager = data.get('manager')
            if manager is not None:
                try:
                    employee.manager = Employee.objects.get(pk=manager)
                except Employee.DoesNotExist:
                    raise ResourceNotFoundException(f"Manager with not found")
            else:
                employee.manager = None
        if 'address_city' in data:
            employee.address_city = data['address_city']
        if 'address_street' in data:
            employee.address_street = data['address_street']
        if 'phone_number' in data:
            employee.phone_number = data.get('phone_number', "")
        if 'email' in data:
            employee.email = data['email']
        if 'positions' in data:
            employee.positions = data.get('positions', "")

        employee.save()
        return employee

    @staticmethod
    def delete_employee(gym_id, employee_id):
        if not Employee.objects.filter(pk=employee_id, gym_id=gym_id).exists():
            raise ResourceNotFoundException(f"Employee with ID {employee_id} not found for gym_id {gym_id}")
        Employee.objects.filter(pk=employee_id, gym_id=gym_id).delete()
