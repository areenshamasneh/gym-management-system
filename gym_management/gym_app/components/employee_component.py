from django.shortcuts import get_object_or_404
from ..models import Employee, Gym


def get_all_employees():
    return Employee.objects.all()


def get_employee_by_id(employee_id):
    return get_object_or_404(Employee, pk=employee_id)


def create_employee(data):
    gym_id = data.get("gym")
    if gym_id is not None:
        gym_instance = get_object_or_404(Gym, pk=gym_id)
        data["gym"] = gym_instance
    else:
        raise ValueError("Gym field is required")

    employee = Employee.objects.create(**data)
    return employee


def update_employee(employee_id, data):
    employee = get_object_or_404(Employee, pk=employee_id)
    gym_id = data.get("gym")

    if gym_id:
        gym_instance = get_object_or_404(Gym, pk=gym_id)
        data["gym"] = gym_instance

    for attr, value in data.items():
        setattr(employee, attr, value)

    employee.save()
    return employee


def delete_employee(employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.delete()
