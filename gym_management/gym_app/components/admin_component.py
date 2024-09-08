from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories.admin_repository import AdminRepository


class AdminComponent:
    def __init__(self, admin_repository=None, logger=None):
        self.repo = admin_repository or AdminRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("AdminComponent initialized")

    def fetch_all_admins(self, gym_id, filter_criteria=None, offset=0, limit=10):
        self.logger.log_info(f"Fetching all admins for gym_id: {gym_id} with filters: {filter_criteria}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        admins, total_admins = self.repo.get_all_admins(gym, filter_criteria, offset, limit)
        if not admins:
            raise ResourceNotFoundException("No admins found for this gym Or this page is empty")

        return admins, total_admins

    def fetch_admin_by_id(self, gym_id, admin_id):
        self.logger.log_info(f"Fetching admin with id: {admin_id} for gym_id: {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        admin = self.repo.get_admin_by_id(gym, admin_id)
        if not admin:
            raise ResourceNotFoundException("Admin not found")

        return admin

    def add_admin(self, gym_id, data):
        self.logger.log_info("Adding new admin")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        admin = self.repo.create_admin(gym, data)
        Session.commit()
        return admin

    def modify_admin(self, gym_id, admin_id, data):
        self.logger.log_info(f"Modifying admin ID {admin_id} for gym_id: {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        admin = self.repo.update_admin(gym, admin_id, data)
        if not admin:
            raise ResourceNotFoundException("Admin not found")

        Session.commit()
        return admin

    def remove_admin(self, gym_id, admin_id):
        self.logger.log_info(f"Removing admin ID {admin_id} for gym_id: {gym_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        success = self.repo.delete_admin(gym, admin_id)
        if not success:
            raise ResourceNotFoundException("Admin not found")

        Session.commit()
        return success
