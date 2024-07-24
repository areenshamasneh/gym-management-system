from gym_app.repositories import (
    get_all_hall_machines,
    get_hall_machine_by_id,
    create_hall_machine,
    update_hall_machine,
    delete_hall_machine,
)


def fetch_all_hall_machines():
    return get_all_hall_machines()


def fetch_hall_machine_by_id(hall_machine_id):
    return get_hall_machine_by_id(hall_machine_id)


def add_hall_machine(data):
    return create_hall_machine(data)


def modify_hall_machine(hall_machine_id, data):
    return update_hall_machine(hall_machine_id, data)


def remove_hall_machine(hall_machine_id):
    delete_hall_machine(hall_machine_id)
