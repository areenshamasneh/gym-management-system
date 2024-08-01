from django.http import Http404
from gym_app.repositories.admin_repository import AdminRepository
from gym_app.logging import SimpleLogger


class AdminComponent:
    def __init__(self, admin_repository=None, logger=None):
        self.admin_repository = admin_repository or AdminRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("AdminComponent initialized")

    def fetch_all_admins(self, gym_id):
        try:
            self.logger.log_info(f"Fetching all admins for gym_id: {gym_id}")
            admins = self.admin_repository.get_all_admins(gym_id)
            return admins
        except Exception as e:
            self.logger.log_error(
                f"Error fetching all admins for gym_id: {gym_id}: {str(e)}"
            )
            raise

    def fetch_admin_by_id(self, gym_id, admin_id):
        try:
            self.logger.log_info(
                f"Fetching admin by ID {admin_id} for gym_id: {gym_id}"
            )
            admin = self.admin_repository.get_admin_by_id(gym_id, admin_id)
            return admin
        except Http404 as e:
            self.logger.log_error(
                f"Admin with ID {admin_id} not found for gym_id {gym_id}: {str(e)}"
            )
            raise
        except Exception as e:
            self.logger.log_error(
                f"Unexpected error fetching admin by ID {admin_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise

    def add_admin(self, gym_id, admin_data):
        try:
            self.logger.log_info(f"Adding new admin for gym_id: {gym_id}")
            admin = self.admin_repository.create_admin(gym_id, admin_data)
            return admin
        except Exception as e:
            self.logger.log_error(f"Error adding admin for gym_id: {gym_id}: {str(e)}")
            raise

    def modify_admin(self, gym_id, admin_id, admin_data):
        try:
            admin = self.admin_repository.get_admin_by_id(gym_id, admin_id)
        except Http404 as e:
            self.logger.log_error(
                f"Admin with ID {admin_id} not found for gym_id {gym_id}: {str(e)}"
            )
            raise ValueError(f"Admin with ID {admin_id} does not exist")

        try:
            self.logger.log_info(f"Modifying admin ID {admin_id} for gym_id: {gym_id}")
            updated_admin = self.admin_repository.update_admin(admin, admin_data)
            return updated_admin
        except Exception as e:
            self.logger.log_error(
                f"Unexpected error modifying admin ID {admin_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise

    def remove_admin(self, gym_id, admin_id):
        try:
            self.logger.log_info(f"Removing admin ID {admin_id} for gym_id: {gym_id}")
            self.admin_repository.delete_admin(gym_id, admin_id)
        except Http404 as e:
            self.logger.log_error(
                f"Admin with ID {admin_id} not found for gym_id {gym_id}: {str(e)}"
            )
            raise
        except Exception as e:
            self.logger.log_error(
                f"Unexpected error removing admin ID {admin_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise
