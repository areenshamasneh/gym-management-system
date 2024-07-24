from gym_app.repositories.machine_repository import (
    get_all_machines,
    get_machine_by_id,
    create_machine,
    update_machine,
    delete_machine,
)


def fetch_all_machines():
    return get_all_machines()


def fetch_machine_by_id(pk):
    return get_machine_by_id(pk)


def add_machine(data):
    return create_machine(data)


def modify_machine(pk, data):
    return update_machine(pk, data)


def remove_machine(pk):
    delete_machine(pk)
