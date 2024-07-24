from gym_app.repositories import (
    get_all_members,
    get_member_by_id,
    create_member,
    update_member,
    delete_member,
)


def fetch_all_members():
    return get_all_members()


def fetch_member_by_id(member_id):
    return get_member_by_id(member_id)


def add_member(data):
    return create_member(data)


def modify_member(member_id, data):
    return update_member(member_id, data)


def remove_member(member_id):
    delete_member(member_id)
