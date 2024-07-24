from gym_app.repositories.admin_repository import (
    get_all_admins,
    get_admin_by_id,
    create_admin,
    update_admin,
    delete_admin,
)


def fetch_all_admins():
    return get_all_admins()


def fetch_admin_by_id(admin_id):
    return get_admin_by_id(admin_id)


def add_admin(data):
    return create_admin(data)


def modify_admin(admin_id, data):
    return update_admin(admin_id, data)


def remove_admin(admin_id):
    delete_admin(admin_id)
