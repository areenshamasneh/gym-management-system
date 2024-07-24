from gym_app.repositories.admin_repository import AdminRepository


class AdminComponent:
    @staticmethod
    def fetch_all_admins():
        return AdminRepository.get_all_admins()

    @staticmethod
    def fetch_admin_by_id(admin_id):
        return AdminRepository.get_admin_by_id(admin_id)

    @staticmethod
    def add_admin(data):
        return AdminRepository.create_admin(data)

    @staticmethod
    def modify_admin(admin_id, data):
        return AdminRepository.update_admin(admin_id, data)

    @staticmethod
    def remove_admin(admin_id):
        return AdminRepository.delete_admin(admin_id)
