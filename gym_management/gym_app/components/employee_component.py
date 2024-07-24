from gym_app.repositories.employee_repository import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee,
)


def fetch_all_employees():
    return get_all_employees()


def fetch_employee_by_id(employee_id):
    return get_employee_by_id(employee_id)


def add_employee(data):
    return create_employee(data)


def modify_employee(employee_id, data):
    return update_employee(employee_id, data)


def remove_employee(employee_id):
    delete_employee(employee_id)
