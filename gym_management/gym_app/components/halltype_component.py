from gym_app.repositories import (
    get_all_hall_types,
    get_hall_type_by_id,
    create_hall_type,
    update_hall_type,
    delete_hall_type,
)


def fetch_all_hall_types():
    return get_all_hall_types()


def fetch_hall_type_by_id(hall_type_id):
    return get_hall_type_by_id(hall_type_id)


def add_hall_type(data):
    return create_hall_type(data)


def modify_hall_type(hall_type_id, data):
    return update_hall_type(hall_type_id, data)


def remove_hall_type(hall_type_id):
    delete_hall_type(hall_type_id)
