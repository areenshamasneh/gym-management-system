from gym_app.logging import CustomLogger
from gym_app.repositories.member_repository import MemberRepository


class MemberComponent:
    def __init__(self, repo: MemberRepository, logger: CustomLogger):
        self.repo = repo
        self.logger = logger

    def fetch_all_members(self, gym_id):
        self.logger.log("Fetching all members")
        return self.repo.get_all_members(gym_id)

    def fetch_member_by_id(self, gym_id, member_id):
        self.logger.log(f"Fetching member with ID {member_id}")
        return self.repo.get_member_by_id(gym_id, member_id)

    def add_member(self, gym_id, data):
        self.logger.log(f"Adding new member with data: {data}")
        try:
            return self.repo.create_member(gym_id, data)
        except ValueError as e:
            raise ValueError("Invalid data") from e

    def modify_member(self, gym_id, member_id, data):
        self.logger.log(f"Modifying member with ID {member_id} with data: {data}")
        return self.repo.update_member(gym_id, member_id, data)

    def remove_member(self, gym_id, member_id):
        self.logger.log(f"Removing member with ID {member_id}")
        return self.repo.delete_member(gym_id, member_id)
