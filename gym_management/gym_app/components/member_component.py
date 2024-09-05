from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.logging import SimpleLogger
from gym_app.repositories.member_repository import MemberRepository


class MemberComponent:
    def __init__(self, repo=None, logger=None):
        self.repo = repo if repo else MemberRepository()
        self.logger = logger if logger else SimpleLogger()
        self.logger.log_info("MemberComponent initialized")

    def fetch_all_members(self, gym_id):
        self.logger.log_info("Fetching all members")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")

        members = self.repo.get_all_members(gym)
        if not members:
            raise ResourceNotFoundException(f"No members found for gym with ID {gym_id}")
        return members

    def fetch_member_by_id(self, gym_id, member_id):
        self.logger.log_info(f"Fetching member with ID {member_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")
        member = self.repo.get_member_by_id(gym, member_id)
        if not member:
            raise ResourceNotFoundException(f"Member with ID {member_id} not found in gym with ID {gym_id}")
        return member

    def create_member(self, gym_id, data):
        self.logger.log_info(f"Adding new member with data: {data}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")
        member = self.repo.create_member(gym, data)
        Session.commit()
        return member

    def modify_member(self, gym_id, member_id, data):
        self.logger.log_info(f"Modifying member with ID {member_id} with data: {data}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")
        member = self.repo.update_member(gym, member_id, data)
        if member:
            Session.commit()
            return member
        raise ResourceNotFoundException(f"Member with ID {member_id} not found in gym with ID {gym_id}")

    def remove_member(self, gym_id, member_id):
        self.logger.log_info(f"Removing member with ID {member_id}")
        gym = self.repo.get_gym(gym_id)
        if not gym:
            raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")
        success = self.repo.delete_member(gym, member_id)
        if success:
            Session.commit()
            return success
        raise ResourceNotFoundException(f"Member with ID {member_id} not found in gym with ID {gym_id}")
