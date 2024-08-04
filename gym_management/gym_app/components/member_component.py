from gym_app.logging import SimpleLogger
from gym_app.repositories.member_repository import MemberRepository
from gym_app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    DatabaseException,
)


class MemberComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else MemberRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("MemberComponent initialized")

    def fetch_all_members(self, gym_id):
        self.logger.log_info("Fetching all members")
        try:
            return self.repo.get_all_members(gym_id)
        except Exception as e:
            self.logger.log_error(f"Error fetching members: {e}")
            raise DatabaseException("An error occurred while fetching all members.")

    def fetch_member_by_id(self, gym_id, member_id):
        self.logger.log_info(f"Fetching member with ID {member_id}")
        try:
            member = self.repo.get_member_by_id(gym_id, member_id)
            if not member:
                raise ResourceNotFoundException(
                    f"Member with ID {member_id} not found."
                )
            return member
        except ResourceNotFoundException:
            self.logger.log_error(f"Member with ID {member_id} not found.")
            raise
        except Exception as e:
            self.logger.log_error(f"Error fetching member by ID: {e}")
            raise DatabaseException(
                "An error occurred while fetching the member by ID."
            )

    def add_member(self, gym_id, data):
        self.logger.log_info(f"Adding new member with data: {data}")
        try:
            return self.repo.create_member(gym_id, data)
        except ValueError as e:
            self.logger.log_error(f"Error adding member: {e}")
            raise ValidationException("Invalid data for member.") from e
        except Exception as e:
            self.logger.log_error(f"Error adding member: {e}")
            raise DatabaseException("An error occurred while adding the member.")

    def modify_member(self, gym_id, member_id, data):
        self.logger.log_info(f"Modifying member with ID {member_id} with data: {data}")
        try:
            member = self.repo.update_member(gym_id, member_id, data)
            if not member:
                raise ResourceNotFoundException(
                    f"Member with ID {member_id} not found."
                )
            return member
        except ResourceNotFoundException:
            self.logger.log_error(f"Member with ID {member_id} not found.")
            raise
        except ValueError as e:
            self.logger.log_error(f"Error modifying member: {e}")
            raise ValidationException("Invalid data for member.") from e
        except Exception as e:
            self.logger.log_error(f"Error modifying member: {e}")
            raise DatabaseException("An error occurred while modifying the member.")

    def remove_member(self, gym_id, member_id):
        self.logger.log_info(f"Removing member with ID {member_id}")
        try:
            if not self.repo.delete_member(gym_id, member_id):
                raise ResourceNotFoundException(
                    f"Member with ID {member_id} not found."
                )
        except ResourceNotFoundException:
            self.logger.log_error(f"Member with ID {member_id} not found.")
            raise
        except Exception as e:
            self.logger.log_error(f"Error removing member: {e}")
            raise DatabaseException("An error occurred while removing the member.")
