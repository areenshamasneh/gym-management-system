from common.db.database import Session
from gym_app.logging import SimpleLogger
from gym_app.repositories.admin_repository import AdminRepository


class AdminComponent:
    def __init__(self, admin_repository=None, logger=None):
        self.admin_repository = admin_repository or AdminRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("AdminComponent initialized")

    def fetch_all_admins(self, gym_id, filter_criteria=None):
        self.logger.log_info(f"Fetching all admins for gym_id: {gym_id} with filters: {filter_criteria}")
        return self.admin_repository.get_all_admins(gym_id, filter_criteria)

    def fetch_admin_by_id(self, gym_id, admin_id):
        self.logger.log_info(f"Fetching admin with id: {admin_id} for gym_id: {gym_id}")
        return self.admin_repository.get_admin_by_id(gym_id, admin_id)

    def add_admin(self, gym_id, data):
        session = Session()
        self.logger.log_info("Adding new admin")
        admin = self.admin_repository.create_admin(gym_id, data)
        session.commit()
        return admin

    def modify_admin(self, gym_id, admin_id, data):
        session = Session()
        self.logger.log_info(f"Modifying admin ID {admin_id} for gym_id: {gym_id}")
        admin = self.admin_repository.update_admin(admin_id, data)
        if admin:
            session.commit()
            return admin
        return None

    def remove_admin(self, gym_id, admin_id):
        session = Session()
        self.logger.log_info(f"Removing admin ID {admin_id} for gym_id: {gym_id}")
        success = self.admin_repository.delete_admin(admin_id)
        if success:
            session.commit()
            return success
        return False
