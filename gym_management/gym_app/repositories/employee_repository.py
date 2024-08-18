from gym_app.models import Employee, Gym


class EmployeeRepository:
    @staticmethod
    def get_all_employees(gym_id):
        return Employee.objects.filter(gym_id=gym_id).select_related('gym', 'manager')

    @staticmethod
    def get_employee_by_id(gym_id, employee_id):
        return Employee.objects.filter(pk=employee_id, gym_id=gym_id).first()

    @staticmethod
    def create_employee(gym_id, data):
        gym = Gym.objects.get(pk=gym_id)
        manager = None
        if 'manager' in data:
            manager = Employee.objects.get(pk=data['manager'])
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

        if 'name' in data:
            employee.name = data['name']
        if 'manager' in data:
            manager = data.get('manager')
            if manager is not None:
                employee.manager = Employee.objects.get(pk=manager)
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
        Employee.objects.filter(pk=employee_id, gym_id=gym_id).delete()
