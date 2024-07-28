from gym_app.repositories.admin_repository import AdminRepository


class AdminComponent:

    def fetch_all_admins(gym_id):
        return AdminRepository.get_all_admins(gym_id)

    def fetch_admin_by_id(gym_id, admin_id):
        return AdminRepository.get_admin_by_id(gym_id, admin_id)

    def add_admin(gym_id, data):
        return AdminRepository.create_admin(gym_id, data)

    def modify_admin(gym_id, admin_id, data):
        return AdminRepository.update_admin(gym_id, admin_id, data)

    def remove_admin(gym_id, admin_id):
        return AdminRepository.delete_admin(gym_id, admin_id)
