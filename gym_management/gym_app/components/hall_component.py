from gym_app.repositories.hall_repository import (
    get_all_halls,
    get_hall_by_id,
    create_hall,
    update_hall,
    delete_hall,
)


def fetch_all_halls():
    return get_all_halls()


def fetch_hall_by_id(hall_id):
    return get_hall_by_id(hall_id)


def add_hall(data):
    return create_hall(data)


def modify_hall(hall_id, data):
    return update_hall(hall_id, data)


def remove_hall(hall_id):
    delete_hall(hall_id)
