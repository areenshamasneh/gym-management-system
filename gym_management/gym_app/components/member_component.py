from gym_app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    DatabaseException,
)
from gym_app.logging import SimpleLogger
from gym_app.repositories.member_repository import MemberRepository


class MemberComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else MemberRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("MemberComponent initialized")

    def fetch_all_members(self, gym_id):
        self.logger.log_info("Fetching all members")
        try:
            return self.repo.get_all_members(gym_id)
        except DatabaseException as e:
            self.logger.log_error(f"Database error fetching members: {e}")
            raise
        except Exception as e:
            self.logger.log_error(f"Unexpected error fetching members: {e}")
            raise DatabaseException("An error occurred while fetching all members.")

    def fetch_member_by_id(self, gym_id, member_id):
        self.logger.log_info(f"Fetching member with ID {member_id}")
        try:
            return self.repo.get_member_by_id(gym_id, member_id)
        except ResourceNotFoundException as e:
            self.logger.log_error(f"Resource not found: {e}")
            raise
        except DatabaseException as e:
            self.logger.log_error(f"Database error: {e}")
            raise
        except Exception as e:
            self.logger.log_error(f"Unexpected error fetching member: {e}")
            raise DatabaseException("An error occurred while fetching the member by ID.")

    def create_member(self, gym_id, data):
        self.logger.log_info(f"Adding new member with data: {data}")
        try:
            return self.repo.create_member(gym_id, data)
        except ValidationException as e:
            self.logger.log_error(f"Validation error: {e}")
            raise
        except DatabaseException as e:
            self.logger.log_error(f"Database error: {e}")
            raise
        except Exception as e:
            self.logger.log_error(f"Unexpected error adding member: {e}")
            raise DatabaseException("An error occurred while adding the member.")

    def modify_member(self, gym_id, member_id, data):
        self.logger.log_info(f"Modifying member with ID {member_id} with data: {data}")
        try:
            return self.repo.update_member(gym_id, member_id, data)
        except ResourceNotFoundException as e:
            self.logger.log_error(f"Resource not found: {e}")
            raise
        except ValidationException as e:
            self.logger.log_error(f"Validation error: {e}")
            raise
        except DatabaseException as e:
            self.logger.log_error(f"Database error: {e}")
            raise
        except Exception as e:
            self.logger.log_error(f"Unexpected error modifying member: {e}")
            raise DatabaseException("An error occurred while modifying the member.")

    def remove_member(self, gym_id, member_id):
        self.logger.log_info(f"Removing member with ID {member_id}")
        try:
            self.repo.delete_member(gym_id, member_id)
        except ResourceNotFoundException as e:
            self.logger.log_error(f"Resource not found: {e}")
            raise
        except DatabaseException as e:
            self.logger.log_error(f"Database error: {e}")
            raise
        except Exception as e:
            self.logger.log_error(f"Unexpected error removing member: {e}")
            raise DatabaseException("An error occurred while removing the member.")
