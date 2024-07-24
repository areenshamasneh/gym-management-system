from gym_app.repositories.gym_repository import (
    get_all_gyms,
    get_gym_by_id,
    create_gym,
    update_gym,
    delete_gym,
)


def fetch_all_gyms():
    return get_all_gyms()


def fetch_gym_by_id(pk):
    return get_gym_by_id(pk)


def add_gym(data):
    return create_gym(data)


def modify_gym(pk, data):
    return update_gym(pk, data)


def remove_gym(pk):
    delete_gym(pk)
