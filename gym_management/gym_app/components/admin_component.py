from gym_app.exceptions import ResourceNotFoundException, DatabaseException
from gym_app.logging import SimpleLogger
from gym_app.repositories.admin_repository import AdminRepository


class AdminComponent:
    def __init__(self, admin_repository=None, logger=None):
        self.admin_repository = admin_repository or AdminRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("AdminComponent initialized")

    def fetch_all_admins(self, gym_id, filter_criteria):
        try:
            self.logger.log_info(f"Fetching all admins for gym_id: {gym_id} with filters: {filter_criteria}")
            admins = self.admin_repository.get_all_admins(gym_id, filter_criteria)
            if not admins:
                raise ResourceNotFoundException(f"There are no admins for gym_id: {gym_id}")
            return admins
        except ResourceNotFoundException as e:
            self.logger.log_error(f"Resource not found for gym_id: {gym_id}: {str(e)}")
            raise e
        except Exception as e:
            self.logger.log_error(f"Error fetching all admins for gym_id: {gym_id}: {str(e)}")
            raise DatabaseException("An error occurred while fetching all admins.")

    def fetch_admin_by_id(self, gym_id, admin_id):
        try:
            self.logger.log_info(
                f"Fetching admin by ID {admin_id} for gym_id: {gym_id}"
            )
            admin = self.admin_repository.get_admin_by_id(gym_id, admin_id)
            if admin is None:
                raise ResourceNotFoundException(f"Admin with ID {admin_id} does not exist for gym_id: {gym_id}")
            return admin
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise ResourceNotFoundException(f"Resource not found for gym_id: {gym_id}")
        except Exception as e:
            self.logger.log_error(
                f"Unexpected error fetching admin by ID {admin_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise DatabaseException(f"Error fetching admin by ID: {str(e)}")

    def add_admin(self, gym_id, admin_data):
        try:
            self.logger.log_info(f"Adding new admin for gym_id: {gym_id}")
            admin = self.admin_repository.create_admin(gym_id, admin_data)
            return admin
        except ResourceNotFoundException as e:
            self.logger.log_error(
                f"Gym with ID {gym_id} not found: {str(e)}"
            )
            raise e
        except Exception as e:
            self.logger.log_error(f"Error adding admin for gym_id: {gym_id}: {str(e)}")
            raise DatabaseException(f"Error adding admin: {str(e)}")

    def modify_admin(self, gym_id, admin_id, admin_data):
        try:
            self.admin_repository.get_admin_by_id(gym_id, admin_id)

            self.logger.log_info(f"Modifying admin ID {admin_id} for gym_id: {gym_id}")
            updated_admin = self.admin_repository.update_admin(gym_id, admin_id, admin_data)
            return updated_admin
        except Exception as e:
            self.logger.log_error(
                f"Unexpected error modifying admin ID {admin_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise DatabaseException(f"Error modifying admin: {str(e)}")

    def remove_admin(self, gym_id, admin_id):
        try:
            self.logger.log_info(f"Removing admin ID {admin_id} for gym_id: {gym_id}")
            return self.admin_repository.delete_admin(gym_id, admin_id)
        except ResourceNotFoundException as e:
            self.logger.log_error(
                f"Admin with ID {admin_id} not found for gym_id {gym_id}: {str(e)}"
            )
            raise e
        except Exception as e:
            self.logger.log_error(
                f"Unexpected error removing admin ID {admin_id} for gym_id: {gym_id}: {str(e)}"
            )
            raise DatabaseException(f"Error removing admin: {str(e)}")
