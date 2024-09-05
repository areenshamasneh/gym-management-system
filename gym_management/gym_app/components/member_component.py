from common.db.database import Session
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
        return self.repo.get_all_members(gym_id)

    def fetch_member_by_id(self, gym_id, member_id):
        self.logger.log_info(f"Fetching member with ID {member_id}")
        return self.repo.get_member_by_id(gym_id, member_id)

    def create_member(self, gym_id, data):
        session = Session()
        self.logger.log_info(f"Adding new member with data: {data}")
        member = self.repo.create_member(gym_id, data)
        session.commit()
        return member

    def modify_member(self, gym_id, member_id, data):
        session = Session()
        self.logger.log_info(f"Modifying member with ID {member_id} with data: {data}")
        member = self.repo.update_member(gym_id, member_id, data)
        if member:
            session.commit()
            return member
        return None

    def remove_member(self, gym_id, member_id):
        session = Session()
        self.logger.log_info(f"Removing member with ID {member_id}")
        success = self.repo.delete_member(gym_id, member_id)
        if success:
            session.commit()
            return success
        return False
