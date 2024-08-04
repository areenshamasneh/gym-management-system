from django.shortcuts import get_object_or_404

from gym_app.models import Employee, Gym


class EmployeeRepository:

    def get_all_employees(self, gym_id):
        return Employee.objects.filter(gym_id=gym_id)

    def get_employee_by_id(self, gym_id, employee_id):
        return get_object_or_404(Employee, pk=employee_id, gym_id=gym_id)

    def create_employee(self, gym_id, data):
        gym = get_object_or_404(Gym, pk=gym_id)
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

    def update_employee(self, gym_id, employee_id, data):
        employee = get_object_or_404(Employee, pk=employee_id, gym_id=gym_id)
        employee.name = data.get("name", employee.name)
        employee.manager_id = data.get("manager_id", employee.manager_id)
        employee.address_city = data.get("address_city", employee.address_city)
        employee.address_street = data.get("address_street", employee.address_street)
        employee.phone_number = data.get("phone_number", employee.phone_number)
        employee.email = data.get("email", employee.email)
        employee.positions = data.get("positions", employee.positions)
        employee.save()
        return employee

    def delete_employee(self, gym_id, employee_id):
        employee = get_object_or_404(Employee, pk=employee_id, gym_id=gym_id)
        employee.delete()
