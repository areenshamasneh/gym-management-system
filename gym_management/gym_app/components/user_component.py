from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories.user_repository import UserRepository


class UserComponent:
    def __init__(self, user_repository=None, logger=None):
        self.repo = user_repository or UserRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("UserComponent initialized")

    def fetch_user_by_id(self, user_id):
        self.logger.log_info(f"Fetching user with id: {user_id}")
        user = self.repo.get_user(user_id)
        if not user:
            raise ResourceNotFoundException("User not found")
        return user

    def add_user(self, data):
        self.logger.log_info("Adding new user")
        user = self.repo.create_user(data)
        Session.commit()
        return user

    def modify_user(self, user_id, data):
        self.logger.log_info(f"Modifying user ID {user_id}")
        user = self.repo.update_user(user_id, data)
        if not user:
            raise ResourceNotFoundException("User not found")
        Session.commit()
        return user

    def remove_user(self, user_id):
        self.logger.log_info(f"Removing user ID {user_id}")
        success = self.repo.delete_user(user_id)
        if not success:
            raise ResourceNotFoundException("User not found")
        Session.commit()
        return success

    def authenticate_user(self, username, password):
        self.logger.log_info(f"Authenticating User :{username}")
        return self.repo.authenticate_user(username, password)

